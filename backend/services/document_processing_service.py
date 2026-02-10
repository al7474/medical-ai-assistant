"""
Document Processing Service for extracting and processing medical documents.
Handles PDF extraction, text cleaning, and document preparation for RAG.
"""

from typing import List, Optional, BinaryIO
from pathlib import Path
import io

from PyPDF2 import PdfReader
from langchain.docstore.document import Document as LangChainDocument

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from models.medical_document import MedicalDocument, DocumentType
from models.user import User
from services.vector_store_service import get_vector_store_service


class DocumentProcessingService:
    """
    Service for processing medical documents and extracting text content.
    Integrates with vector store for RAG functionality.
    """
    
    def __init__(self, db: AsyncSession):
        """
        Initialize the document processing service.
        
        Args:
            db: Database session
        """
        self.db = db
        self.vector_store = get_vector_store_service()
    
    async def process_pdf(
        self,
        file_content: bytes,
        filename: str,
        user_id: int,
        document_type: DocumentType,
        title: Optional[str] = None,
        description: Optional[str] = None
    ) -> MedicalDocument:
        """
        Process a PDF file and store it with embeddings.
        
        Args:
            file_content: PDF file content as bytes
            filename: Original filename
            user_id: ID of the user who owns the document
            document_type: Type of medical document
            title: Optional document title
            description: Optional document description
            
        Returns:
            Created MedicalDocument instance
        """
        # Extract text from PDF
        text_content = self._extract_text_from_pdf(file_content)
        
        if not text_content or len(text_content.strip()) < 10:
            raise ValueError("Could not extract meaningful text from PDF")
        
        # Create MedicalDocument record
        medical_doc = MedicalDocument(
            user_id=user_id,
            document_type=document_type,
            title=title or filename,
            description=description,
            file_path=f"uploads/{user_id}/{filename}",  # Placeholder path
            file_size=len(file_content),
            mime_type="application/pdf"
        )
        
        # Save to database
        self.db.add(medical_doc)
        await self.db.commit()
        await self.db.refresh(medical_doc)
        
        # Create embeddings if vector store is available
        if self.vector_store.is_available():
            try:
                # Create LangChain document
                langchain_doc = LangChainDocument(
                    page_content=text_content,
                    metadata={
                        "document_id": medical_doc.id,
                        "document_type": document_type.value,
                        "title": medical_doc.title,
                        "source": filename,
                        "user_id": user_id
                    }
                )
                
                # Add to vector store
                num_chunks = self.vector_store.add_documents(
                    [langchain_doc],
                    user_id=user_id,
                    collection_name=f"medical_documents"
                )
                
                # Update document status
                medical_doc.embeddings_created = True
                medical_doc.processing_status = "completed"
                
                await self.db.commit()
                
                print(f"✅ Created {num_chunks} embeddings for document {medical_doc.id}")
                
            except Exception as e:
                print(f"⚠️ Error creating embeddings: {e}")
                medical_doc.processing_status = "failed"
                await self.db.commit()
        else:
            print("⚠️ Vector store not available. Document saved without embeddings.")
            medical_doc.processing_status = "pending"
            await self.db.commit()
        
        return medical_doc
    
    async def process_text_document(
        self,
        text_content: str,
        user_id: int,
        document_type: DocumentType,
        title: str,
        description: Optional[str] = None
    ) -> MedicalDocument:
        """
        Process a text document and store it with embeddings.
        
        Args:
            text_content: Document text content
            user_id: ID of the user who owns the document
            document_type: Type of medical document
            title: Document title
            description: Optional document description
            
        Returns:
            Created MedicalDocument instance
        """
        if not text_content or len(text_content.strip()) < 10:
            raise ValueError("Text content is too short or empty")
        
        # Create MedicalDocument record
        medical_doc = MedicalDocument(
            user_id=user_id,
            document_type=document_type,
            title=title,
            description=description,
            file_path=None,  # No file for text documents
            file_size=len(text_content.encode('utf-8')),
            mime_type="text/plain"
        )
        
        # Save to database
        self.db.add(medical_doc)
        await self.db.commit()
        await self.db.refresh(medical_doc)
        
        # Create embeddings if vector store is available
        if self.vector_store.is_available():
            try:
                # Create LangChain document
                langchain_doc = LangChainDocument(
                    page_content=text_content,
                    metadata={
                        "document_id": medical_doc.id,
                        "document_type": document_type.value,
                        "title": medical_doc.title,
                        "source": "text_input",
                        "user_id": user_id
                    }
                )
                
                # Add to vector store
                num_chunks = self.vector_store.add_documents(
                    [langchain_doc],
                    user_id=user_id,
                    collection_name=f"medical_documents"
                )
                
                # Update document status
                medical_doc.embeddings_created = True
                medical_doc.processing_status = "completed"
                
                await self.db.commit()
                
                print(f"✅ Created {num_chunks} embeddings for text document {medical_doc.id}")
                
            except Exception as e:
                print(f"⚠️ Error creating embeddings: {e}")
                medical_doc.processing_status = "failed"
                await self.db.commit()
        else:
            print("⚠️ Vector store not available. Document saved without embeddings.")
            medical_doc.processing_status = "pending"
            await self.db.commit()
        
        return medical_doc
    
    async def get_relevant_documents(
        self,
        query: str,
        user_id: int,
        k: int = 3
    ) -> List[dict]:
        """
        Get relevant documents for a query using RAG.
        
        Args:
            query: Search query
            user_id: ID of the user
            k: Number of documents to retrieve
            
        Returns:
            List of relevant document metadata
        """
        if not self.vector_store.is_available():
            return []
        
        # Search vector store
        relevant_docs = self.vector_store.search_by_user(query, user_id, k=k)
        
        # Extract metadata
        results = []
        for doc in relevant_docs:
            results.append({
                "document_id": doc.metadata.get("document_id"),
                "title": doc.metadata.get("title"),
                "document_type": doc.metadata.get("document_type"),
                "content_excerpt": doc.page_content[:200] + "..." if len(doc.page_content) > 200 else doc.page_content
            })
        
        return results
    
    async def get_context_for_chat(
        self,
        query: str,
        user_id: int,
        k: int = 3
    ) -> str:
        """
        Get formatted context from documents for chat.
        
        Args:
            query: User's chat message
            user_id: ID of the user
            k: Number of documents to retrieve
            
        Returns:
            Formatted context string
        """
        if not self.vector_store.is_available():
            return ""
        
        context = self.vector_store.get_context_for_query(query, user_id, k=k)
        
        if context:
            return f"\n\n===RELEVANT MEDICAL DOCUMENTS===\n{context}\n==================================="
        
        return ""
    
    async def reprocess_document(
        self,
        document_id: int,
        user_id: int
    ) -> bool:
        """
        Reprocess a document to create/update embeddings.
        
        Args:
            document_id: ID of the document to reprocess
            user_id: ID of the user (for verification)
            
        Returns:
            True if successful
        """
        # Get document
        result = await self.db.execute(
            select(MedicalDocument).where(
                MedicalDocument.id == document_id,
                MedicalDocument.user_id == user_id
            )
        )
        document = result.scalar_one_or_none()
        
        if not document:
            return False
        
        # TODO: Implement reprocessing logic
        # This would require storing the original file content
        # For now, just mark as pending
        document.processing_status = "pending"
        await self.db.commit()
        
        return True
    
    def _extract_text_from_pdf(self, file_content: bytes) -> str:
        """
        Extract text from PDF file.
        
        Args:
            file_content: PDF file content as bytes
            
        Returns:
            Extracted text
        """
        try:
            pdf_file = io.BytesIO(file_content)
            pdf_reader = PdfReader(pdf_file)
            
            # Extract text from all pages
            text_parts = []
            for page_num, page in enumerate(pdf_reader.pages, 1):
                page_text = page.extract_text()
                if page_text:
                    text_parts.append(f"[Page {page_num}]\n{page_text}")
            
            full_text = "\n\n".join(text_parts)
            return full_text.strip()
            
        except Exception as e:
            print(f"Error extracting PDF text: {e}")
            raise ValueError(f"Failed to extract text from PDF: {str(e)}")
    
    def _clean_text(self, text: str) -> str:
        """
        Clean extracted text.
        
        Args:
            text: Raw text
            
        Returns:
            Cleaned text
        """
        # Remove excessive whitespace
        lines = [line.strip() for line in text.split('\n')]
        lines = [line for line in lines if line]  # Remove empty lines
        
        return '\n'.join(lines)


# Factory function
def get_document_processing_service(db: AsyncSession) -> DocumentProcessingService:
    """
    Factory function to create DocumentProcessingService instance.
    
    Args:
        db: Database session
        
    Returns:
        DocumentProcessingService instance
    """
    return DocumentProcessingService(db)
