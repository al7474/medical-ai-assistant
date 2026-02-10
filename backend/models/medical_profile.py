"""
Medical Profile Model
Stores comprehensive medical information for each user
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, JSON, Enum as SQLEnum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from .base import Base


class BloodType(str, enum.Enum):
    """Blood type enumeration"""
    A_POSITIVE = "A+"
    A_NEGATIVE = "A-"
    B_POSITIVE = "B+"
    B_NEGATIVE = "B-"
    AB_POSITIVE = "AB+"
    AB_NEGATIVE = "AB-"
    O_POSITIVE = "O+"
    O_NEGATIVE = "O-"
    UNKNOWN = "Unknown"


class MedicalProfile(Base):
    """
    Medical Profile for users
    Contains critical medical information for AI context
    """
    __tablename__ = "medical_profiles"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    
    # Basic Medical Info
    blood_type = Column(SQLEnum(BloodType), default=BloodType.UNKNOWN)
    height_cm = Column(Integer, nullable=True)  # Height in centimeters
    weight_kg = Column(Integer, nullable=True)  # Weight in kilograms
    date_of_birth = Column(DateTime, nullable=True)
    
    # Medical History
    allergies = Column(JSON, default=list)  # List of allergies ["Penicillin", "Peanuts"]
    chronic_conditions = Column(JSON, default=list)  # ["Diabetes", "Hypertension"]
    current_medications = Column(JSON, default=list)  # [{"name": "Aspirin", "dosage": "100mg", "frequency": "daily"}]
    past_surgeries = Column(JSON, default=list)  # [{"name": "Appendectomy", "date": "2020-01-15"}]
    
    # Family History
    family_history = Column(JSON, default=dict)  # {"diabetes": ["father"], "cancer": ["mother"]}
    
    # Lifestyle
    smoking_status = Column(String(50), nullable=True)  # "never", "former", "current"
    alcohol_consumption = Column(String(50), nullable=True)  # "none", "occasional", "moderate", "heavy"
    exercise_frequency = Column(String(50), nullable=True)  # "sedentary", "light", "moderate", "active"
    
    # Emergency Contact
    emergency_contact = Column(JSON, default=dict)  # {"name": "John Doe", "phone": "+1234567890", "relation": "spouse"}
    
    # Additional Notes
    notes = Column(Text, nullable=True)  # Additional medical notes
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    user = relationship("User", back_populates="medical_profile")
    
    def __repr__(self):
        return f"<MedicalProfile(user_id={self.user_id}, blood_type={self.blood_type})>"
    
    def to_context_dict(self) -> dict:
        """
        Convert profile to a dictionary suitable for AI context
        Returns only relevant, non-null information
        """
        context = {}
        
        if self.blood_type and self.blood_type != BloodType.UNKNOWN:
            context["blood_type"] = self.blood_type.value
        
        if self.height_cm and self.weight_kg:
            bmi = round(self.weight_kg / ((self.height_cm / 100) ** 2), 1)
            context["bmi"] = bmi
            context["height"] = f"{self.height_cm}cm"
            context["weight"] = f"{self.weight_kg}kg"
        
        if self.date_of_birth:
            age = (datetime.utcnow() - self.date_of_birth).days // 365
            context["age"] = age
        
        if self.allergies:
            context["allergies"] = self.allergies
        
        if self.chronic_conditions:
            context["chronic_conditions"] = self.chronic_conditions
        
        if self.current_medications:
            context["current_medications"] = [
                f"{med.get('name')} {med.get('dosage', '')}".strip()
                for med in self.current_medications
            ]
        
        if self.smoking_status:
            context["smoking_status"] = self.smoking_status
        
        if self.alcohol_consumption:
            context["alcohol_consumption"] = self.alcohol_consumption
        
        return context
