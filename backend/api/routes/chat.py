"""
Chat endpoints
"""

from fastapi import APIRouter, HTTPException
from schemas.chat import ChatRequest, ChatResponse
from services.chat_service import get_chat_service

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("/", response_model=ChatResponse)
async def chat(message: ChatRequest):
    """
    Chat with AI medical assistant
    
    Now powered by LangChain + LLM (OpenAI GPT or Anthropic Claude)
    
    To enable AI:
    1. Get API key from https://platform.openai.com/api-keys
    2. Add to .env file: OPENAI_API_KEY=sk-...
    3. Restart server
    """
    user_text = message.text
    
    if not user_text:
        raise HTTPException(status_code=400, detail="Message text is required")
    
    # Get chat service
    chat_svc = get_chat_service()
    
    # Optional: Add context (user info, medical history, etc.)
    context = {
        "user_info": "General consultation"
    }
    
    # Get AI response
    bot_response = await chat_svc.chat(user_text, context)
    
    return ChatResponse(
        user_message=user_text,
        bot_response=bot_response,
        status="ok",
        ai_enabled=chat_svc.is_available(),
        provider=chat_svc.provider if chat_svc.is_available() else "fallback",
        model=chat_svc.model_name if chat_svc.is_available() else "simple"
    )
