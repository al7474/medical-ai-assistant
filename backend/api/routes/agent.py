"""
Agent Chat API Routes
Intelligent agent-powered chat endpoints
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from typing import Optional, List, Dict

from models import User
from models.conversation import MessageRole
from api.deps import get_db, get_current_user
from services.langgraph_agent_service import get_agent_service
from services.medical_context_service import get_medical_context_service

router = APIRouter(prefix="/agent", tags=["agent"])


class AgentChatRequest(BaseModel):
    """Request for agent chat"""
    message: str
    conversation_id: Optional[int] = None
    use_context: bool = True


class AgentChatResponse(BaseModel):
    """Response from agent chat"""
    response: str
    conversation_id: Optional[int] = None
    tools_used: Optional[List[str]] = None


@router.post("/chat", response_model=AgentChatResponse)
async def agent_chat(
    request: AgentChatRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Chat with the intelligent agent.
    The agent can use tools to:
    - Search medical documents
    - Access medical profile
    - View and create appointments
    - List documents
    
    **Authentication:** Required (JWT token)
    """
    try:
        # Get agent service
        agent_service = get_agent_service(db)
        
        if not agent_service.is_available():
            raise HTTPException(
                status_code=503,
                detail="Agent service not available. Please configure OpenAI or Anthropic API key."
            )
        
        # Get user context if requested
        user_context = None
        conversation_history = None
        
        if request.use_context:
            context_service = get_medical_context_service(db)
            
            # Get medical context
            medical_context = await context_service.get_formatted_context(current_user.id)
            if medical_context:
                user_context = medical_context
            
            # Get conversation history
            if request.conversation_id:
                conv_history = await context_service.get_recent_conversation_history(
                    user_id=current_user.id,
                    conversation_id=request.conversation_id,
                    limit=10
                )
                if conv_history:
                    conversation_history = [
                        {"role": msg.role.value, "content": msg.content}
                        for msg in conv_history
                    ]
        
        # Run the agent
        response = await agent_service.run(
            user_message=request.message,
            user_id=current_user.id,
            user_context=user_context,
            conversation_history=conversation_history
        )
        
        # Save to conversation if conversation_id provided
        conversation_id = request.conversation_id
        if request.use_context:
            context_service = get_medical_context_service(db)
            
            # Save user message
            user_msg = await context_service.save_conversation_message(
                user_id=current_user.id,
                role=MessageRole.USER,
                content=request.message,
                conversation_id=conversation_id
            )
            
            # Get conversation_id from first message if not provided
            if not conversation_id:
                conversation_id = user_msg.conversation_id
            
            # Save agent response
            await context_service.save_conversation_message(
                user_id=current_user.id,
                role=MessageRole.ASSISTANT,
                content=response,
                conversation_id=conversation_id,
                ai_provider="langgraph_agent",
                ai_model=agent_service.provider
            )
        
        return AgentChatResponse(
            response=response,
            conversation_id=conversation_id,
            tools_used=[]  # TODO: Extract tools used from agent execution
        )
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Agent chat error: {e}")
        raise HTTPException(status_code=500, detail=f"Agent error: {str(e)}")


@router.get("/capabilities")
async def get_agent_capabilities(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get the agent's capabilities (available tools).
    
    **Authentication:** Required (JWT token)
    """
    from services.agent_tools import AGENT_TOOLS
    
    capabilities = []
    for tool in AGENT_TOOLS:
        capabilities.append({
            "name": tool.name,
            "description": tool.description,
            "parameters": tool.args_schema.schema() if tool.args_schema else {}
        })
    
    return {
        "agent_available": True,
        "capabilities": capabilities,
        "provider": get_agent_service(db).provider if get_agent_service(db).is_available() else None
    }


@router.post("/test-tool/{tool_name}")
async def test_tool(
    tool_name: str,
    parameters: Dict,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Test a specific tool directly (for development/debugging).
    
    **Authentication:** Required (JWT token)
    """
    from services.agent_tools import AGENT_TOOLS, initialize_tools
    
    # Initialize tools
    initialize_tools(db)
    
    # Find the tool
    tool = None
    for t in AGENT_TOOLS:
        if t.name == tool_name:
            tool = t
            break
    
    if not tool:
        raise HTTPException(status_code=404, detail=f"Tool '{tool_name}' not found")
    
    try:
        # Add user_id to parameters if not present
        if "user_id" in tool.args_schema.schema()["properties"] and "user_id" not in parameters:
            parameters["user_id"] = current_user.id
        
        # Call the tool
        result = await tool.ainvoke(parameters)
        
        return {
            "tool": tool_name,
            "parameters": parameters,
            "result": result
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Tool execution error: {str(e)}")
