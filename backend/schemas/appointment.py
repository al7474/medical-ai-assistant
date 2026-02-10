"""
Appointment Pydantic schemas for request/response validation
"""

from pydantic import BaseModel, ConfigDict


class AppointmentCreate(BaseModel):
    """Schema for creating a new appointment"""
    user_id: int
    description: str


class AppointmentRead(BaseModel):
    """Schema for reading appointment data"""
    id: int
    user_id: int
    description: str
    
    model_config = ConfigDict(from_attributes=True)
