
"""
Medical AI Assistant - Simple API for Learning
Phase 1: Basic backend without database

This is your starting point. A simple REST API with FastAPI.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


# Create the FastAPI application
app = FastAPI(
    title="Medical AI Assistant",
    description="My intelligent medical assistant - Learning step by step",
    version="0.1.0"
)

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


# Startup message when you run the server
if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting Medical AI Assistant...")
    print("📖 Documentation: http://localhost:8000/docs")
    uvicorn.run(app, host="0.0.0.0", port=8000)
