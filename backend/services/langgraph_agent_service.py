"""
LangGraph Agent Service
Intelligent agent with tool calling and multi-step reasoning
"""

from typing import Optional, Dict, Any, List, Annotated
from datetime import datetime
import json

from langchain_core.messages import HumanMessage, AIMessage, SystemMessage, ToolMessage
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from typing_extensions import TypedDict

from sqlalchemy.ext.asyncio import AsyncSession

from services.agent_tools import AGENT_TOOLS, initialize_tools
from config import settings


class AgentState(TypedDict):
    """State for the agent graph"""
    messages: Annotated[List, add_messages]
    user_id: int
    user_context: Optional[str]


class LangGraphAgentService:
    """
    LangGraph-based agent with tool calling capabilities.
    Handles multi-step reasoning and autonomous task execution.
    """
    
    def __init__(self, db: AsyncSession):
        """
        Initialize the agent service
        
        Args:
            db: Database session for tool access
        """
        self.db = db
        self.llm = None
        self.agent_executor = None
        self._initialize_llm()
        self._build_graph()
        
        # Initialize tools with database session
        initialize_tools(db)
    
    def _initialize_llm(self):
        """Initialize the language model with tool binding"""
        openai_key = settings.OPENAI_API_KEY
        anthropic_key = settings.ANTHROPIC_API_KEY
        gemini_key = settings.GEMINI_API_KEY
        
        if openai_key:
            # Use OpenAI (best for tool calling)
            self.llm = ChatOpenAI(
                model="gpt-4o-mini",
                temperature=0,
                api_key=openai_key
            )
            self.provider = "openai"
        elif gemini_key:
            # Use Google Gemini (good for tool calling)
            self.llm = ChatGoogleGenerativeAI(
                model="gemini-1.5-flash",
                temperature=0,
                google_api_key=gemini_key
            )
            self.provider = "gemini"
        elif anthropic_key:
            # Use Anthropic
            self.llm = ChatAnthropic(
                model="claude-3-5-sonnet-20241022",
                temperature=0,
                api_key=anthropic_key
            )
            self.provider = "anthropic"
        else:
            raise ValueError("No AI provider API key configured. Set OPENAI_API_KEY, GEMINI_API_KEY, or ANTHROPIC_API_KEY")
        
        # Bind tools to the LLM
        self.llm_with_tools = self.llm.bind_tools(AGENT_TOOLS)
    
    def _build_graph(self):
        """Build the LangGraph workflow"""
        # Create the graph
        workflow = StateGraph(AgentState)
        
        # Add nodes
        workflow.add_node("agent", self._call_model)
        workflow.add_node("tools", ToolNode(AGENT_TOOLS))
        
        # Set entry point
        workflow.set_entry_point("agent")
        
        # Add conditional edges
        workflow.add_conditional_edges(
            "agent",
            tools_condition,
            {
                # If tools should be called, go to tools node
                "tools": "tools",
                # If no tools, end
                END: END
            }
        )
        
        # After tools are executed, go back to agent
        workflow.add_edge("tools", "agent")
        
        # Compile the graph
        self.agent_executor = workflow.compile()
    
    async def _call_model(self, state: AgentState) -> Dict[str, Any]:
        """
        Call the language model with current state
        
        Args:
            state: Current agent state
        
        Returns:
            Updated state with model response
        """
        messages = state["messages"]
        
        # Add system message with user context if available
        if state.get("user_context"):
            system_msg = SystemMessage(content=self._build_system_prompt(state["user_context"]))
            messages_with_system = [system_msg] + messages
        else:
            messages_with_system = messages
        
        # Call the model
        response = await self.llm_with_tools.ainvoke(messages_with_system)
        
        return {"messages": [response]}
    
    def _build_system_prompt(self, user_context: Optional[str] = None) -> str:
        """Build the system prompt for the agent"""
        base_prompt = """You are an intelligent medical assistant with access to tools that help you provide accurate and helpful information to patients.

**Your Capabilities:**
- Search through the patient's medical documents
- Access their medical profile (conditions, medications, allergies)
- View and create appointments
- List uploaded medical documents
- Get current date and time information

**Guidelines:**
1. **Use tools proactively**: When the user asks about their medical history, appointments, or documents, use the appropriate tools to get accurate information
2. **Multi-step reasoning**: Break down complex requests into steps and use multiple tools if needed
3. **Be thorough**: Always check the medical profile and relevant documents before giving medical advice
4. **Safety first**: Always remind users to consult with healthcare professionals for serious concerns
5. **Privacy**: Respect patient confidentiality and only access information relevant to the query
6. **Clear communication**: Explain what tools you're using and why, in a user-friendly manner

**Tool Usage Examples:**
- If asked about medications → Use `get_user_medical_profile`
- If asked about test results → Use `search_medical_documents`
- If asked about appointments → Use `get_upcoming_appointments`
- If asked to schedule → Use `create_appointment` (get date/time details first)
- If need current date → Use `get_current_date_time`

**Interaction Style:**
- Empathetic and professional
- Use medical terminology appropriately but explain complex terms
- Provide context from their medical history when relevant
- Ask clarifying questions when needed
"""
        
        if user_context:
            base_prompt += f"\n\n**PATIENT CONTEXT:**\n{user_context}\n"
            base_prompt += "\nUse this context along with your tools to provide personalized assistance."
        
        return base_prompt
    
    async def run(
        self,
        user_message: str,
        user_id: int,
        user_context: Optional[str] = None,
        conversation_history: Optional[List[Dict[str, str]]] = None
    ) -> str:
        """
        Run the agent with a user message
        
        Args:
            user_message: The user's input message
            user_id: ID of the user
            user_context: Optional medical context about the user
            conversation_history: Optional previous conversation messages
        
        Returns:
            Agent's response
        """
        try:
            # Build initial state
            messages = []
            
            # Add conversation history if provided
            if conversation_history:
                for msg in conversation_history[-10:]:  # Last 10 messages
                    if msg["role"] == "user":
                        messages.append(HumanMessage(content=msg["content"]))
                    elif msg["role"] == "assistant":
                        messages.append(AIMessage(content=msg["content"]))
            
            # Add current message
            messages.append(HumanMessage(content=user_message))
            
            # Create initial state
            state: AgentState = {
                "messages": messages,
                "user_id": user_id,
                "user_context": user_context
            }
            
            # Run the agent
            result = await self.agent_executor.ainvoke(state)
            
            # Extract final response
            final_messages = result["messages"]
            
            # Get the last AI message
            for msg in reversed(final_messages):
                if isinstance(msg, AIMessage):
                    return msg.content
            
            return "I apologize, but I couldn't generate a response. Please try again."
            
        except Exception as e:
            print(f"❌ Agent execution error: {e}")
            return f"I apologize, but I encountered an error: {str(e)}. Please try again."
    
    def is_available(self) -> bool:
        """Check if the agent service is available"""
        return self.llm is not None and self.agent_executor is not None


# Singleton instance holder
_agent_service: Optional[LangGraphAgentService] = None


def get_agent_service(db: AsyncSession) -> LangGraphAgentService:
    """
    Get or create the agent service singleton
    
    Args:
        db: Database session
    
    Returns:
        Agent service instance
    """
    global _agent_service
    
    # Note: In production, you might want to create a new instance per request
    # or use dependency injection. For now, we create a new one each time.
    return LangGraphAgentService(db)
