"""
User Pydantic schemas for request/response validation
"""

from pydantic import BaseModel, ConfigDict, EmailStr


class UserCreate(BaseModel):
    """Schema for creating a new user"""
    name: str
    email: str


class UserRead(BaseModel):
    """Schema for reading user data"""
    id: int
    name: str
    email: str
    
    model_config = ConfigDict(from_attributes=True)
