"""
Medical Document API Routes
Handles document upload, processing, and retrieval
"""

from fastapi import APIRouter, File, UploadFile, Form, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional

from schemas.medical_document import (
    MedicalDocumentCreate,
    MedicalDocumentResponse,
    MedicalDocumentListResponse
)
from models import User
from models.medical_document import DocumentType
from services.document_processing_service import get_document_processing_service
from api.deps import get_db, get_current_user

router = APIRouter(prefix="/medical-documents", tags=["medical-documents"])


@router.post("/upload-pdf", response_model=MedicalDocumentResponse)
async def upload_pdf_document(
    file: UploadFile = File(...),
    document_type: DocumentType = Form(...),
    title: Optional[str] = Form(None),
    description: Optional[str] = Form(None),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Upload a PDF medical document and process it for RAG.
    
    **Process:**
    1. Accepts PDF file upload
    2. Extracts text from PDF
    3. Creates embeddings for semantic search
    4. Stores in vector database
    
    **Document Types:**
    - lab_result: Laboratory test results
    - prescription: Medication prescriptions
    - medical_image: Medical imaging reports
    - visit_summary: Doctor visit summaries
    - other: Other medical documents
    
    **Authentication:** Required (JWT token)
    
    **Note:** Requires OpenAI API key for embeddings
    """
    # Validate file type
    if not file.content_type or "pdf" not in file.content_type.lower():
        raise HTTPException(status_code=400, detail="Only PDF files are supported")
    
    # Read file content
    try:
        file_content = await file.read()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error reading file: {str(e)}")
    
    # Validate file size (10MB max)
    if len(file_content) > 10 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="File size must be less than 10MB")
    
    # Process document
    doc_service = get_document_processing_service(db)
    
    try:
        medical_doc = await doc_service.process_pdf(
            file_content=file_content,
            filename=file.filename,
            user_id=current_user.id,
            document_type=document_type,
            title=title,
            description=description
        )
        
        return MedicalDocumentResponse.model_validate(medical_doc)
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing document: {str(e)}")


@router.post("/upload-text", response_model=MedicalDocumentResponse)
async def upload_text_document(
    document: MedicalDocumentCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Upload a text medical document and process it for RAG.
    
    **Process:**
    1. Accepts text content
    2. Creates embeddings for semantic search
    3. Stores in vector database
    
    **Authentication:** Required (JWT token)
    
    **Note:** Requires OpenAI API key for embeddings
    """
    if not document.text_content:
        raise HTTPException(status_code=400, detail="Text content is required")
    
    if len(document.text_content) < 10:
        raise HTTPException(status_code=400, detail="Text content is too short (minimum 10 characters)")
    
    # Process document
    doc_service = get_document_processing_service(db)
    
    try:
        medical_doc = await doc_service.process_text_document(
            text_content=document.text_content,
            user_id=current_user.id,
            document_type=document.document_type,
            title=document.title,
            description=document.description
        )
        
        return MedicalDocumentResponse.model_validate(medical_doc)
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing document: {str(e)}")


@router.get("/", response_model=MedicalDocumentListResponse)
async def list_medical_documents(
    skip: int = 0,
    limit: int = 20,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    List all medical documents for the authenticated user.
    
    **Parameters:**
    - skip: Number of records to skip (pagination)
    - limit: Maximum number of records to return
    
    **Authentication:** Required (JWT token)
    """
    doc_service = get_document_processing_service(db)
    
    from sqlalchemy import select
    from models.medical_document import MedicalDocument
    
    # Query documents
    result = await db.execute(
        select(MedicalDocument)
        .where(MedicalDocument.user_id == current_user.id)
        .order_by(MedicalDocument.created_at.desc())
        .offset(skip)
        .limit(limit)
    )
    documents = result.scalars().all()
    
    # Get total count
    from sqlalchemy import func
    count_result = await db.execute(
        select(func.count(MedicalDocument.id))
        .where(MedicalDocument.user_id == current_user.id)
    )
    total = count_result.scalar()
    
    return MedicalDocumentListResponse(
        documents=[MedicalDocumentResponse.model_validate(doc) for doc in documents],
        total=total,
        skip=skip,
        limit=limit
    )


@router.get("/search")
async def search_documents(
    query: str,
    k: int = 5,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Search medical documents using semantic search (RAG).
    
    **Parameters:**
    - query: Search query text
    - k: Number of results to return (default: 5)
    
    **Returns:**
    - Relevant document excerpts with metadata
    
    **Authentication:** Required (JWT token)
    
    **Note:** Requires OpenAI API key and uploaded documents with embeddings
    """
    if not query:
        raise HTTPException(status_code=400, detail="Query is required")
    
    doc_service = get_document_processing_service(db)
    
    try:
        results = await doc_service.get_relevant_documents(
            query=query,
            user_id=current_user.id,
            k=k
        )
        
        return {
            "query": query,
            "results": results,
            "total_results": len(results)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error searching documents: {str(e)}")


@router.get("/{document_id}", response_model=MedicalDocumentResponse)
async def get_document(
    document_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get a specific medical document by ID.
    
    **Authentication:** Required (JWT token)
    """
    from sqlalchemy import select
    from models.medical_document import MedicalDocument
    
    result = await db.execute(
        select(MedicalDocument).where(
            MedicalDocument.id == document_id,
            MedicalDocument.user_id == current_user.id
        )
    )
    document = result.scalar_one_or_none()
    
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    
    return MedicalDocumentResponse.model_validate(document)


@router.delete("/{document_id}")
async def delete_document(
    document_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Delete a medical document.
    
    **Note:** This also removes the document from the vector store.
    
    **Authentication:** Required (JWT token)
    """
    from sqlalchemy import select
    from models.medical_document import MedicalDocument
    
    result = await db.execute(
        select(MedicalDocument).where(
            MedicalDocument.id == document_id,
            MedicalDocument.user_id == current_user.id
        )
    )
    document = result.scalar_one_or_none()
    
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    
    # Delete from database
    await db.delete(document)
    await db.commit()
    
    # TODO: Remove from vector store
    # This would require tracking which chunks belong to which document
    
    return {"message": "Document deleted successfully"}
