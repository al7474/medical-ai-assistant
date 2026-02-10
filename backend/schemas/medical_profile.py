"""
Pydantic schemas for medical profile endpoints
"""
from pydantic import BaseModel, Field, field_validator
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum


class BloodTypeEnum(str, Enum):
    """Blood type options"""
    A_POSITIVE = "A+"
    A_NEGATIVE = "A-"
    B_POSITIVE = "B+"
    B_NEGATIVE = "B-"
    AB_POSITIVE = "AB+"
    AB_NEGATIVE = "AB-"
    O_POSITIVE = "O+"
    O_NEGATIVE = "O-"
    UNKNOWN = "Unknown"


class MedicationSchema(BaseModel):
    """Schema for current medication"""
    name: str
    dosage: Optional[str] = None
    frequency: Optional[str] = None
    notes: Optional[str] = None


class SurgerySchema(BaseModel):
    """Schema for past surgery"""
    name: str
    date: Optional[str] = None
    notes: Optional[str] = None


class EmergencyContactSchema(BaseModel):
    """Schema for emergency contact"""
    name: str
    phone: str
    relation: Optional[str] = None


# Request schemas
class MedicalProfileCreate(BaseModel):
    """Create medical profile"""
    blood_type: Optional[BloodTypeEnum] = BloodTypeEnum.UNKNOWN
    height_cm: Optional[int] = Field(None, ge=50, le=300)
    weight_kg: Optional[int] = Field(None, ge=20, le=500)
    date_of_birth: Optional[datetime] = None
    allergies: Optional[List[str]] = []
    chronic_conditions: Optional[List[str]] = []
    current_medications: Optional[List[MedicationSchema]] = []
    past_surgeries: Optional[List[SurgerySchema]] = []
    family_history: Optional[Dict[str, List[str]]] = {}
    smoking_status: Optional[str] = None
    alcohol_consumption: Optional[str] = None
    exercise_frequency: Optional[str] = None
    emergency_contact: Optional[EmergencyContactSchema] = None
    notes: Optional[str] = None


class MedicalProfileUpdate(BaseModel):
    """Update medical profile (all fields optional)"""
    blood_type: Optional[BloodTypeEnum] = None
    height_cm: Optional[int] = Field(None, ge=50, le=300)
    weight_kg: Optional[int] = Field(None, ge=20, le=500)
    date_of_birth: Optional[datetime] = None
    allergies: Optional[List[str]] = None
    chronic_conditions: Optional[List[str]] = None
    current_medications: Optional[List[Dict[str, Any]]] = None
    past_surgeries: Optional[List[Dict[str, Any]]] = None
    family_history: Optional[Dict[str, List[str]]] = None
    smoking_status: Optional[str] = None
    alcohol_consumption: Optional[str] = None
    exercise_frequency: Optional[str] = None
    emergency_contact: Optional[Dict[str, str]] = None
    notes: Optional[str] = None


# Response schemas
class MedicalProfileResponse(BaseModel):
    """Medical profile response"""
    id: int
    user_id: int
    blood_type: BloodTypeEnum
    height_cm: Optional[int]
    weight_kg: Optional[int]
    date_of_birth: Optional[datetime]
    allergies: List[str]
    chronic_conditions: List[str]
    current_medications: List[Dict[str, Any]]
    past_surgeries: List[Dict[str, Any]]
    family_history: Dict[str, List[str]]
    smoking_status: Optional[str]
    alcohol_consumption: Optional[str]
    exercise_frequency: Optional[str]
    emergency_contact: Optional[Dict[str, str]]
    notes: Optional[str]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class MedicalProfileContext(BaseModel):
    """Simplified profile for AI context"""
    blood_type: Optional[str] = None
    bmi: Optional[float] = None
    height: Optional[str] = None
    weight: Optional[str] = None
    age: Optional[int] = None
    allergies: Optional[List[str]] = None
    chronic_conditions: Optional[List[str]] = None
    current_medications: Optional[List[str]] = None
    smoking_status: Optional[str] = None
    alcohol_consumption: Optional[str] = None
