"""
Application configuration
"""
import os
from typing import Optional


class Settings:
    """Application settings"""
    
    # App info
    APP_NAME: str = "Medical AI Assistant"
    APP_VERSION: str = "0.2.0"
    APP_DESCRIPTION: str = "My intelligent medical assistant - Learning step by step"
    
    # Database
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "postgresql+asyncpg://postgres:postgres@localhost:5433/medical_assistant"
    )
    
    # AI Configuration
    AI_PROVIDER: str = os.getenv("AI_PROVIDER", "openai").lower()
    AI_MODEL: str = os.getenv("AI_MODEL", "gpt-3.5-turbo")
    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")
    ANTHROPIC_API_KEY: Optional[str] = os.getenv("ANTHROPIC_API_KEY")
    
    # CORS
    ALLOWED_ORIGINS: list = ["*"]  # In production, specify allowed origins
    
    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000


settings = Settings()
