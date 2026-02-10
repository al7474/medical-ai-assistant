
"""
Medical AI Assistant - Simple API for Learning
Phase 1: Basic backend without database

This is your starting point. A simple REST API with FastAPI.
"""


from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from typing import List
from pydantic import BaseModel, ConfigDict
import models
import database
from startup import lifespan


# Create the FastAPI application

app = FastAPI(
    title="Medical AI Assistant",
    description="My intelligent medical assistant - Learning step by step",
    version="0.1.0",
    lifespan=lifespan
)
# ==================== ENDPOINTS ====================

# --- User CRUD Models ---
class UserCreate(BaseModel):
    name: str
    email: str

class UserRead(BaseModel):
    id: int
    name: str
    email: str
    model_config = ConfigDict(from_attributes=True)

# --- Appointment CRUD Models ---
class AppointmentCreate(BaseModel):
    user_id: int
    description: str

class AppointmentRead(BaseModel):
    id: int
    user_id: int
    description: str
    model_config = ConfigDict(from_attributes=True)

# --- User CRUD Endpoints ---
@app.post("/users/", response_model=UserRead)
async def create_user(user: UserCreate, db: AsyncSession = Depends(database.get_db)):
    new_user = models.User(name=user.name, email=user.email)
    db.add(new_user)
    try:
        await db.commit()
        await db.refresh(new_user)
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=400, detail="Email already registered")
    return new_user

@app.get("/users/", response_model=List[UserRead])
async def list_users(db: AsyncSession = Depends(database.get_db)):
    result = await db.execute(select(models.User))
    users = result.scalars().all()
    return users

# --- Appointment CRUD Endpoints ---
@app.post("/appointments/", response_model=AppointmentRead)
async def create_appointment(
    appointment: AppointmentCreate, 
    db: AsyncSession = Depends(database.get_db)
):
    """Create a new appointment"""
    # Verify user exists
    user_result = await db.execute(
        select(models.User).where(models.User.id == appointment.user_id)
    )
    user = user_result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    new_appointment = models.Appointment(
        user_id=appointment.user_id,
        description=appointment.description
    )
    db.add(new_appointment)
    await db.commit()
    await db.refresh(new_appointment)
    return new_appointment

@app.get("/appointments/", response_model=List[AppointmentRead])
async def list_appointments(db: AsyncSession = Depends(database.get_db)):
    """List all appointments"""
    result = await db.execute(select(models.Appointment))
    appointments = result.scalars().all()
    return appointments

@app.get("/appointments/{appointment_id}", response_model=AppointmentRead)
async def get_appointment(
    appointment_id: int, 
    db: AsyncSession = Depends(database.get_db)
):
    """Get a specific appointment by ID"""
    result = await db.execute(
        select(models.Appointment).where(models.Appointment.id == appointment_id)
    )
    appointment = result.scalar_one_or_none()
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return appointment

@app.delete("/appointments/{appointment_id}")
async def delete_appointment(
    appointment_id: int,
    db: AsyncSession = Depends(database.get_db)
):
    """Delete an appointment"""
    result = await db.execute(
        select(models.Appointment).where(models.Appointment.id == appointment_id)
    )
    appointment = result.scalar_one_or_none()
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    
    await db.delete(appointment)
    await db.commit()
    return {"message": "Appointment deleted successfully", "id": appointment_id}

# Configure CORS to allow requests from the frontend (to be added later)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==================== ENDPOINTS ====================

@app.get("/")
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


@app.get("/health")
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


@app.get("/hello/{name}")
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


@app.post("/chat")
def chat(message: dict):
    """
    Receives a message and responds (no AI yet)

    In the future, this endpoint will use LangGraph and LLM for
    intelligent responses.

    Example usage in /docs:
    {
        "text": "Hello, I need help"
    }
    """
    user_text = message.get("text", "")

    # Simple predefined responses (no AI yet)
    responses = {
        "hello": "Hello! 👋 I am your medical assistant. How can I help you?",
        "help": "I can help you with:\n- General medical information\n- Scheduling appointments\n- Symptom questions",
        "appointment": "To schedule an appointment, I will need some details. What type of specialist do you need?",
        "symptoms": "Please describe your symptoms and I will help you with general information.",
    }

    # Look for keyword in the message
    response = "I am a simple medical assistant (for now). Ask me about appointments, symptoms, or help. 🤖"
    for keyword, reply in responses.items():
        if keyword in user_text.lower():
            response = reply
            break

    return {
        "user_message": user_text,
        "bot_response": response,
        "status": "ok",
        "note": "This is a simple response. Real AI coming soon!"
    }


@app.get("/info")
def system_info():
    """
    Shows project information and next steps
    """
    return {
        "project": "Medical AI Assistant",
        "current_phase": "Phase 1 - Basic Backend ✅",
        "description": "Medical assistant that converses with patients and manages appointments",
        "features_completed": [
            "✅ REST API working",
            "✅ Basic endpoints",
            "✅ Automatic documentation",
            "✅ CORS configured"
        ],
        "next_steps": [
            "⏳ Connect to PostgreSQL",
            "⏳ Add authentication (JWT)",
            "⏳ Integrate AI (LangGraph + LLM)",
            "⏳ Appointment system",
            "⏳ WebSocket for real-time chat",
            "⏳ Frontend with Next.js"
        ],
        "tech_stack": {
            "backend": "FastAPI",
            "database": "PostgreSQL (coming soon)",
            "ai": "LangGraph + LLM (coming soon)",
            "frontend": "Next.js (coming soon)"
        }
    }


@app.get("/test-responses")
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


@app.get("/stats")
async def get_statistics(db: AsyncSession = Depends(database.get_db)):
    """
    Get system statistics - number of users, appointments, etc.
    """
    # Count users
    user_result = await db.execute(select(models.User))
    total_users = len(user_result.scalars().all())
    
    # Count appointments
    appointment_result = await db.execute(select(models.Appointment))
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


# Startup message when you run the server
if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting Medical AI Assistant...")
    print("📖 Documentation: http://localhost:8000/docs")
    uvicorn.run(app, host="0.0.0.0", port=8000)
