"""
System information endpoints
"""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models import User, Appointment
from services.chat_service import get_chat_service
from api.deps import get_db

router = APIRouter(tags=["system"])


@router.get("/")
def read_root():
    """
    Root endpoint - Checks if the API is working

    Try it at: http://localhost:8000
    """
    return {
        "message": "🏥 Welcome to the Medical AI Assistant",
        "status": "online",
        "version": "0.1.0",
        "docs": "http://localhost:8000/docs"
    }


@router.get("/health")
def health_check():
    """
    Checks the API health status

    Useful for monitoring and verifying everything is working.
    """
    return {
        "status": "healthy",
        "service": "medical-ai-assistant",
        "message": "✅ Everything is working correctly"
    }


@router.get("/hello/{name}")
def greet_user(name: str):
    """
    Greets the user by name

    Example: http://localhost:8000/hello/John
    """
    return {
        "message": f"Hello {name}! 👋",
        "greeting": f"Welcome to the medical assistant",
        "tip": "Soon I will be able to help you with real medical queries"
    }


@router.get("/info")
def system_info():
    """
    Shows project information and next steps
    """
    chat_svc = get_chat_service()
    
    return {
        "project": "Medical AI Assistant",
        "current_phase": "Phase 3 - AI Integration ✅" if chat_svc.is_available() else "Phase 2 - Backend Ready ✅",
        "description": "Medical assistant that converses with patients and manages appointments",
        "features_completed": [
            "✅ REST API working",
            "✅ PostgreSQL database",
            "✅ CRUD operations (users, appointments)",
            "✅ Auto database initialization",
            "✅ Statistics endpoint",
            "✅ AI Chat Service" + (" (ENABLED ✨)" if chat_svc.is_available() else " (Waiting for API key)")
        ],
        "ai_status": {
            "available": chat_svc.is_available(),
            "provider": chat_svc.provider if chat_svc.is_available() else "none",
            "model": chat_svc.model_name if chat_svc.is_available() else "none",
            "setup_guide": "Add OPENAI_API_KEY to .env file to enable AI" if not chat_svc.is_available() else "AI is ready!"
        },
        "next_steps": [
            "✅ Connect to PostgreSQL",
            "✅ Add AI integration",
            "⏳ Add authentication (JWT)",
            "⏳ WebSocket for real-time chat",
            "⏳ Frontend with Next.js"
        ],
        "tech_stack": {
            "backend": "FastAPI",
            "database": "PostgreSQL (port 5433)",
            "ai": f"LangChain + {chat_svc.provider} ({chat_svc.model_name})" if chat_svc.is_available() else "LangChain (not configured)",
            "frontend": "Next.js (coming soon)"
        }
    }


@router.get("/test-responses")
def test_responses():
    """
    Test endpoint to see different bot responses
    """
    return {
        "message": "These are the keywords I currently understand:",
        "keywords": [
            "hello - Initial greeting",
            "help - Shows what I can do",
            "appointment - Information about appointments",
            "symptoms - Symptom questions"
        ],
        "example": "Try sending 'hello' to the /chat endpoint"
    }


@router.get("/stats")
async def get_statistics(db: AsyncSession = Depends(get_db)):
    """
    Get system statistics - number of users, appointments, etc.
    """
    # Count users
    user_result = await db.execute(select(User))
    total_users = len(user_result.scalars().all())
    
    # Count appointments
    appointment_result = await db.execute(select(Appointment))
    total_appointments = len(appointment_result.scalars().all())
    
    return {
        "status": "operational",
        "database": "connected",
        "statistics": {
            "total_users": total_users,
            "total_appointments": total_appointments,
        },
        "message": "📊 System statistics retrieved successfully"
    }
