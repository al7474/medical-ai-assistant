"""
Chat endpoints
"""

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.chat import ChatRequest, ChatResponse
from services.chat_service import get_chat_service
from services.medical_context_service import get_medical_context_service
from services.document_processing_service import get_document_processing_service
from models import User, MessageRole
from api.deps import get_db, get_current_user

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("/", response_model=ChatResponse)
async def chat(
    message: ChatRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Chat with AI medical assistant with personalized medical context
    
    **Features:**
    - Uses your medical profile for personalized responses
    - Automatically saves conversation history
    - References your allergies, medications, and conditions
    - Powered by LangChain + LLM (OpenAI GPT or Anthropic Claude)
    
    **Authentication:** Required (JWT token)
    
    **To enable AI:**
    1. Get API key from https://platform.openai.com/api-keys
    2. Add to .env file: OPENAI_API_KEY=sk-...
    3. Restart server
    """
    user_text = message.text
    
    if not user_text:
        raise HTTPException(status_code=400, detail="Message text is required")
    
    # Get services
    chat_svc = get_chat_service()
    context_service = get_medical_context_service(db)
    document_service = get_document_processing_service(db)
    
    # Get user medical context
    user_context = await context_service.get_full_context(
        current_user, 
        include_history=True,
        history_limit=3
    )
    formatted_context = context_service.format_context_for_prompt(user_context)
    
    # Get relevant documents for RAG (if available)
    rag_context = ""
    try:
        rag_context = await document_service.get_context_for_chat(
            query=user_text,
            user_id=current_user.id,
            k=3  # Retrieve top 3 relevant documents
        )
    except Exception as e:
        print(f"⚠️  RAG context retrieval failed: {e}")
    
    # Save user message
    conversation_id = None
    try:
        user_msg = await context_service.save_conversation_message(
            user_id=current_user.id,
            role=MessageRole.USER,
            content=user_text,
            conversation_id=conversation_id
        )
        conversation_id = user_msg.conversation_id
    except Exception as e:
        print(f"⚠️  Failed to save user message: {e}")
    
    # Get AI response with medical context and RAG
    bot_response = await chat_svc.chat(
        user_text, 
        formatted_context=formatted_context,
        rag_context=rag_context if rag_context else None
    )
    
    # Save AI response
    try:
        await context_service.save_conversation_message(
            user_id=current_user.id,
            role=MessageRole.ASSISTANT,
            content=bot_response,
            conversation_id=conversation_id,
            ai_provider=chat_svc.provider if chat_svc.is_available() else "fallback",
            ai_model=chat_svc.model_name if chat_svc.is_available() else "simple",
            context_snapshot=formatted_context[:500]
        )
    except Exception as e:
        print(f"⚠️  Failed to save AI response: {e}")
    
    return ChatResponse(
        user_message=user_text,
        bot_response=bot_response,
        status="ok",
        ai_enabled=chat_svc.is_available(),
        provider=chat_svc.provider if chat_svc.is_available() else "fallback",
        model=chat_svc.model_name if chat_svc.is_available() else "simple"
    )
