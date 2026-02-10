"""
Medical Document Model
Stores medical documents, lab results, prescriptions, etc.
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean, Enum as SQLEnum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from .base import Base


class DocumentType(str, enum.Enum):
    """Types of medical documents"""
    LAB_RESULT = "lab_result"
    PRESCRIPTION = "prescription"
    IMAGING = "imaging"  # X-ray, MRI, CT scan
    MEDICAL_REPORT = "medical_report"
    VACCINATION_RECORD = "vaccination_record"
    DISCHARGE_SUMMARY = "discharge_summary"
    OTHER = "other"


class MedicalDocument(Base):
    """
    Medical documents uploaded by users
    Can be processed for RAG context
    """
    __tablename__ = "medical_documents"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Document metadata
    document_type = Column(SQLEnum(DocumentType), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    
    # File information
    file_path = Column(String(500), nullable=False)  # Path to stored file
    file_name = Column(String(255), nullable=False)  # Original filename
    file_size = Column(Integer, nullable=False)  # Size in bytes
    mime_type = Column(String(100), nullable=False)  # "application/pdf", "image/jpeg", etc.
    
    # Document date (when the document was created/issued, not uploaded)
    document_date = Column(DateTime, nullable=True)
    
    # Processing status
    is_processed = Column(Boolean, default=False)  # Has it been processed for RAG?
    extracted_text = Column(Text, nullable=True)  # Extracted text content
    
    # Vector embeddings (for RAG)
    has_embeddings = Column(Boolean, default=False)
    embedding_ids = Column(Text, nullable=True)  # JSON array of vector store IDs
    
    # Access control
    is_archived = Column(Boolean, default=False)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    user = relationship("User", back_populates="medical_documents")
    
    def __repr__(self):
        return f"<MedicalDocument(id={self.id}, title={self.title}, type={self.document_type})>"
    
    def to_dict(self):
        """Convert document to dictionary for API responses"""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "document_type": self.document_type.value,
            "title": self.title,
            "description": self.description,
            "file_name": self.file_name,
            "file_size": self.file_size,
            "mime_type": self.mime_type,
            "document_date": self.document_date.isoformat() if self.document_date else None,
            "is_processed": self.is_processed,
            "has_embeddings": self.has_embeddings,
            "is_archived": self.is_archived,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
