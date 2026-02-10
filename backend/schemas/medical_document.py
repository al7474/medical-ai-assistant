"""
Pydantic schemas for medical documents
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum


class DocumentTypeEnum(str, Enum):
    """Document type options"""
    LAB_RESULT = "lab_result"
    PRESCRIPTION = "prescription"
    IMAGING = "imaging"
    MEDICAL_REPORT = "medical_report"
    VACCINATION_RECORD = "vaccination_record"
    DISCHARGE_SUMMARY = "discharge_summary"
    OTHER = "other"


# Request schemas
class MedicalDocumentCreate(BaseModel):
    """Create medical document (metadata)"""
    document_type: DocumentTypeEnum
    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    document_date: Optional[datetime] = None


class MedicalDocumentUpdate(BaseModel):
    """Update medical document"""
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    document_type: Optional[DocumentTypeEnum] = None
    document_date: Optional[datetime] = None
    is_archived: Optional[bool] = None


# Response schemas
class MedicalDocumentResponse(BaseModel):
    """Medical document response"""
    id: int
    user_id: int
    document_type: DocumentTypeEnum
    title: str
    description: Optional[str]
    file_name: str
    file_size: int
    mime_type: str
    document_date: Optional[datetime]
    is_processed: bool
    has_embeddings: bool
    is_archived: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class MedicalDocumentList(BaseModel):
    """List of medical documents"""
    total: int
    documents: List[MedicalDocumentResponse]


class DocumentUploadResponse(BaseModel):
    """Response after uploading document"""
    id: int
    file_name: str
    file_size: int
    message: str
