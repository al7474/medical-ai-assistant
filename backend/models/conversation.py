"""
Conversation History Model
Stores all chat conversations for context and history
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean, Enum as SQLEnum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from .base import Base


class MessageRole(str, enum.Enum):
    """Role of message sender"""
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


class Conversation(Base):
    """
    Conversation session between user and AI
    Groups related messages together
    """
    __tablename__ = "conversations"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Conversation metadata
    title = Column(String(255), nullable=True)  # Auto-generated or user-defined title
    summary = Column(Text, nullable=True)  # AI-generated summary of conversation
    
    # Status
    is_active = Column(Boolean, default=True)  # False when conversation is archived
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    user = relationship("User", back_populates="conversations")
    messages = relationship("Message", back_populates="conversation", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Conversation(id={self.id}, user_id={self.user_id}, title={self.title})>"


class Message(Base):
    """
    Individual message in a conversation
    Stores user queries and AI responses
    """
    __tablename__ = "messages"
    
    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(Integer, ForeignKey("conversations.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Message content
    role = Column(SQLEnum(MessageRole), nullable=False)
    content = Column(Text, nullable=False)
    
    # AI metadata (for assistant messages)
    ai_provider = Column(String(50), nullable=True)  # "openai", "anthropic", "fallback"
    ai_model = Column(String(100), nullable=True)  # "gpt-4", "claude-3-sonnet", etc.
    tokens_used = Column(Integer, nullable=True)  # Track token usage
    
    # Context used (snapshot of what context was provided to AI)
    context_snapshot = Column(Text, nullable=True)  # JSON string of context used
    
    # Feedback
    user_rating = Column(Integer, nullable=True)  # 1-5 rating from user
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    
    # Relationships
    conversation = relationship("Conversation", back_populates="messages")
    
    def __repr__(self):
        return f"<Message(id={self.id}, role={self.role}, conversation_id={self.conversation_id})>"
    
    def to_dict(self):
        """Convert message to dictionary for API responses"""
        return {
            "id": self.id,
            "conversation_id": self.conversation_id,
            "role": self.role.value,
            "content": self.content,
            "ai_provider": self.ai_provider,
            "ai_model": self.ai_model,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "user_rating": self.user_rating
        }
