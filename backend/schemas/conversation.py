"""
Pydantic schemas for conversation history
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum


class MessageRoleEnum(str, Enum):
    """Message role options"""
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


# Request schemas
class ConversationCreate(BaseModel):
    """Create new conversation"""
    title: Optional[str] = None


class ConversationUpdate(BaseModel):
    """Update conversation"""
    title: Optional[str] = None
    is_active: Optional[bool] = None


class MessageCreate(BaseModel):
    """Create new message in conversation"""
    content: str = Field(..., min_length=1, max_length=5000)
    role: MessageRoleEnum = MessageRoleEnum.USER


class MessageRating(BaseModel):
    """Rate a message"""
    rating: int = Field(..., ge=1, le=5)


# Response schemas
class MessageResponse(BaseModel):
    """Message response"""
    id: int
    conversation_id: int
    role: MessageRoleEnum
    content: str
    ai_provider: Optional[str]
    ai_model: Optional[str]
    tokens_used: Optional[int]
    user_rating: Optional[int]
    created_at: datetime
    
    class Config:
        from_attributes = True


class ConversationResponse(BaseModel):
    """Conversation response"""
    id: int
    user_id: int
    title: Optional[str]
    summary: Optional[str]
    is_active: bool
    created_at: datetime
    updated_at: datetime
    message_count: Optional[int] = 0
    
    class Config:
        from_attributes = True


class ConversationWithMessages(BaseModel):
    """Conversation with all messages"""
    id: int
    user_id: int
    title: Optional[str]
    summary: Optional[str]
    is_active: bool
    created_at: datetime
    updated_at: datetime
    messages: List[MessageResponse]
    
    class Config:
        from_attributes = True


class ConversationList(BaseModel):
    """List of conversations"""
    total: int
    conversations: List[ConversationResponse]
