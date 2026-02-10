"""
Pydantic schemas for request/response validation
"""

from .user import UserCreate, UserRead
from .appointment import AppointmentCreate, AppointmentRead
from .chat import ChatRequest, ChatResponse
from .auth import UserRegister, UserLogin, Token, TokenData, UserResponse

__all__ = [
    "UserCreate",
    "UserRead",
    "AppointmentCreate",
    "AppointmentRead",
    "ChatRequest",
    "ChatResponse",
    "UserRegister",
    "UserLogin",
    "Token",
    "TokenData",
    "UserResponse",
]
