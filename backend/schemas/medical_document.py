"""
Pydantic schemas for medical documents
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from models.medical_document import DocumentType


# Request schemas
class MedicalDocumentCreate(BaseModel):
    """Create medical document (text content)"""
    document_type: DocumentType
    title: Optional[str] = Field(None, max_length=200)
    description: Optional[str] = None
    text_content: str = Field(..., description="Text content of the document")


class MedicalDocumentUpdate(BaseModel):
    """Update medical document"""
    title: Optional[str] = Field(None, max_length=200)
    description: Optional[str] = None
    document_type: Optional[DocumentType] = None


# Response schemas
class MedicalDocumentResponse(BaseModel):
    """Medical document response"""
    id: int
    user_id: int
    document_type: DocumentType
    title: Optional[str]
    description: Optional[str]
    filename: Optional[str]
    file_path: Optional[str]
    file_size: Optional[int]
    mime_type: Optional[str]
    processing_status: str
    embeddings_created: bool
    created_at: datetime
    updated_at: datetime
    
    model_config = {
        "from_attributes": True
    }


class MedicalDocumentListResponse(BaseModel):
    """Paginated list of medical documents"""
    documents: List[MedicalDocumentResponse]
    total: int
    skip: int
    limit: int

