"""
Authentication Pydantic schemas
"""

from pydantic import BaseModel, field_validator
from datetime import datetime
from typing import Optional
import re


class UserRegister(BaseModel):
    """Schema for user registration"""
    name: str
    email: str
    password: str
    
    @field_validator('email')
    @classmethod
    def validate_email(cls, v: str) -> str:
        """Validate email format"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(pattern, v):
            raise ValueError('Invalid email format')
        return v.lower()


class UserLogin(BaseModel):
    """Schema for user login"""
    email: str
    password: str


class Token(BaseModel):
    """Schema for token response"""
    access_token: str
    token_type: str


class TokenData(BaseModel):
    """Schema for token payload data"""
    email: Optional[str] = None


class UserResponse(BaseModel):
    """Schema for user response (without password)"""
    id: int
    name: str
    email: str
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True
