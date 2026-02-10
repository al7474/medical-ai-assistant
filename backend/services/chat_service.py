"""
AI Chat Service using LangChain
Supports OpenAI (GPT) and Anthropic (Claude)
"""
import os
from typing import Optional, Dict, Any
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage


class ChatService:
    """
    AI Chat Service for Medical Assistant
    Handles conversations with context and memory
    """
    
    def __init__(self):
        self.provider = os.getenv("AI_PROVIDER", "openai").lower()
        self.model_name = os.getenv("AI_MODEL", "gpt-3.5-turbo")
        self.llm = None
        self._initialize_llm()
        
    def _initialize_llm(self):
        """Initialize the LLM based on provider"""
        try:
            if self.provider == "openai":
                api_key = os.getenv("OPENAI_API_KEY")
                if not api_key or api_key == "sk-your-openai-api-key-here":
                    raise ValueError("OpenAI API key not configured")
                self.llm = ChatOpenAI(
                    model=self.model_name,
                    temperature=0.7,
                    openai_api_key=api_key
                )
                print(f"✅ AI Service initialized with OpenAI ({self.model_name})")
                
            elif self.provider == "anthropic":
                api_key = os.getenv("ANTHROPIC_API_KEY")
                if not api_key or api_key.startswith("sk-ant-your"):
                    raise ValueError("Anthropic API key not configured")
                self.llm = ChatAnthropic(
                    model=self.model_name,
                    temperature=0.7,
                    anthropic_api_key=api_key
                )
                print(f"✅ AI Service initialized with Anthropic ({self.model_name})")
                
            else:
                raise ValueError(f"Unknown AI provider: {self.provider}")
                
        except Exception as e:
            print(f"⚠️  AI Service not available: {e}")
            print("💡 Set OPENAI_API_KEY or ANTHROPIC_API_KEY in .env file")
            self.llm = None
    
    def is_available(self) -> bool:
        """Check if AI service is available"""
        return self.llm is not None
    
    async def chat(
        self, 
        message: str, 
        context: Optional[Dict[str, Any]] = None,
        formatted_context: Optional[str] = None
    ) -> str:
        """
        Send a message to the AI and get a response
        
        Args:
            message: User's message
            context: Optional context dictionary (legacy support)
            formatted_context: Pre-formatted context string (preferred)
            
        Returns:
            AI's response as string
        """
        if not self.is_available():
            return self._fallback_response(message)
        
        try:
            # Build system message with context
            system_prompt = self._build_system_prompt(
                context=context,
                formatted_context=formatted_context
            )
            
            # Create messages
            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=message)
            ]
            
            # Get AI response
            response = await self.llm.ainvoke(messages)
            
            return response.content
            
        except Exception as e:
            print(f"❌ AI Chat error: {e}")
            return f"Sorry, I encountered an error: {str(e)}"
    
    def _build_system_prompt(
        self, 
        context: Optional[Dict[str, Any]] = None,
        formatted_context: Optional[str] = None
    ) -> str:
        """Build system prompt with medical context"""
        base_prompt = """You are a helpful medical assistant AI. Your role is to:

1. Answer general medical questions in a friendly, informative way
2. Help users understand their health conditions and medications
3. Provide information about symptoms and when to seek care
4. Be empathetic and professional
5. Use the patient's medical history to provide personalized advice

CRITICAL SAFETY GUIDELINES:
- You are NOT a replacement for professional medical diagnosis or treatment
- Always recommend consulting with a healthcare provider for diagnosis and treatment
- Be clear when something requires immediate medical attention (e.g., chest pain, difficulty breathing, severe bleeding)
- Never suggest stopping or changing medications without consulting a doctor
- Maintain patient confidentiality and privacy

INTERACTION STYLE:
- Be warm, empathetic, and professional
- Acknowledge the patient's concerns
- Reference their medical history when relevant (allergies, conditions, medications)
- Provide clear, actionable information
- Keep responses concise but informative (2-3 paragraphs max)
- Ask clarifying questions when needed"""

        # Add formatted medical context if available
        if formatted_context:
            base_prompt += f"\n\n{'='*50}\nPATIENT MEDICAL CONTEXT:\n{'='*50}\n{formatted_context}\n{'='*50}"
            base_prompt += "\n\nIMPORTANT: Use this context to personalize your responses. Reference allergies when discussing medications, consider chronic conditions when giving advice, etc."
        elif context:
            # Legacy support for old context format
            user_info = context.get("user_info", "")
            if user_info:
                base_prompt += f"\n\nUser context: {user_info}"
        
        return base_prompt
    
    def _fallback_response(self, message: str) -> str:
        """Fallback responses when AI is not available"""
        message_lower = message.lower()
        
        responses = {
            "hello": "Hello! 👋 I'm your medical assistant. How can I help you today?",
            "hi": "Hi there! 👋 How can I assist you?",
            "help": """I can help you with:
            
• General medical information
• Scheduling appointments
• Questions about symptoms
• Information about treatments

What would you like to know?""",
            "appointment": "To schedule an appointment, I'll need some information. What type of specialist do you need to see?",
            "symptoms": "Please describe your symptoms in detail. When did they start? How severe are they?",
        }
        
        # Find matching keyword
        for keyword, response in responses.items():
            if keyword in message_lower:
                return response
        
        return """I'm currently running in simple mode without AI. 
        
To enable AI features:
1. Get an API key from OpenAI (https://platform.openai.com/api-keys)
2. Add it to your .env file: OPENAI_API_KEY=sk-...
3. Restart the server

For now, I can respond to: hello, help, appointment, symptoms"""


# Global chat service instance
chat_service = ChatService()


def get_chat_service() -> ChatService:
    """Get the global chat service instance"""
    return chat_service
