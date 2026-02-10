"""
Chat Pydantic schemas for request/response validation
"""

from pydantic import BaseModel
from typing import Optional


class ChatRequest(BaseModel):
    """Schema for chat request"""
    text: str


class ChatResponse(BaseModel):
    """Schema for chat response"""
    user_message: str
    bot_response: str
    status: str
    ai_enabled: bool
    provider: str
    model: str
