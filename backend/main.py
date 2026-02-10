"""
Medical AI Assistant - Main Application

A professional FastAPI backend for a medical assistant with AI capabilities.
Refactored with proper separation of concerns:
- models/: SQLAlchemy database models
- schemas/: Pydantic request/response models
- api/routes/: API endpoints organized by domain
- services/: Business logic and external services
- core/: Application lifecycle and configuration
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import settings
from core import lifespan
from api.routes import users, appointments, chat, system, auth


# Create the FastAPI application
app = FastAPI(
    title=settings.APP_NAME,
    description=settings.APP_DESCRIPTION,
    version=settings.APP_VERSION,
    lifespan=lifespan
)

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Include routers
app.include_router(system.router)
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(appointments.router)
app.include_router(chat.router)


# Startup message when you run the server
if __name__ == "__main__":
    import uvicorn
    print(f"🚀 Starting {settings.APP_NAME}...")
    print(f"📖 Documentation: http://localhost:{settings.PORT}/docs")
    uvicorn.run(app, host=settings.HOST, port=settings.PORT)
