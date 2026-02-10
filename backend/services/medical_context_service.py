"""
Medical Context Service
Aggregates user medical information for AI context
"""
from typing import Optional, Dict, Any, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import desc
from datetime import datetime, timedelta

from models import User, MedicalProfile, Conversation, Message, MessageRole


class MedicalContextService:
    """
    Service to aggregate and format user medical context for AI
    """
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def get_full_context(
        self, 
        user: User,
        include_history: bool = True,
        history_limit: int = 5
    ) -> Dict[str, Any]:
        """
        Get complete medical context for a user
        
        Args:
            user: User object
            include_history: Include recent conversation history
            history_limit: Number of recent messages to include
            
        Returns:
            Dictionary with all relevant context
        """
        context = {
            "user": {
                "name": user.name,
                "user_id": user.id
            }
        }
        
        # Get medical profile
        medical_profile = await self._get_medical_profile(user.id)
        if medical_profile:
            context["medical_profile"] = medical_profile
        
        # Get recent conversation history
        if include_history:
            history = await self._get_recent_history(user.id, limit=history_limit)
            if history:
                context["recent_history"] = history
        
        return context
    
    async def _get_medical_profile(self, user_id: int) -> Optional[Dict[str, Any]]:
        """Get medical profile context"""
        result = await self.db.execute(
            select(MedicalProfile).where(MedicalProfile.user_id == user_id)
        )
        profile = result.scalar_one_or_none()
        
        if not profile:
            return None
        
        # Use the to_context_dict method from the model
        return profile.to_context_dict()
    
    async def _get_recent_history(self, user_id: int, limit: int = 5) -> List[Dict[str, str]]:
        """
        Get recent conversation history
        Returns last N messages from most recent conversation
        """
        # Get most recent active conversation
        conv_result = await self.db.execute(
            select(Conversation)
            .where(
                Conversation.user_id == user_id,
                Conversation.is_active == True
            )
            .order_by(desc(Conversation.updated_at))
            .limit(1)
        )
        conversation = conv_result.scalar_one_or_none()
        
        if not conversation:
            return []
        
        # Get recent messages from this conversation
        msg_result = await self.db.execute(
            select(Message)
            .where(Message.conversation_id == conversation.id)
            .order_by(desc(Message.created_at))
            .limit(limit)
        )
        messages = msg_result.scalars().all()
        
        # Format messages (reverse to chronological order)
        history = []
        for msg in reversed(messages):
            history.append({
                "role": msg.role.value,
                "content": msg.content[:200] + "..." if len(msg.content) > 200 else msg.content,
                "timestamp": msg.created_at.isoformat() if msg.created_at else None
            })
        
        return history
    
    def format_context_for_prompt(self, context: Dict[str, Any]) -> str:
        """
        Format context dictionary into a readable string for AI prompt
        
        Args:
            context: Context dictionary from get_full_context
            
        Returns:
            Formatted string suitable for system prompt
        """
        parts = []
        
        # User info
        if "user" in context:
            user_info = context["user"]
            parts.append(f"Patient: {user_info['name']}")
        
        # Medical profile
        if "medical_profile" in context:
            profile = context["medical_profile"]
            parts.append("\nMedical Profile:")
            
            if "age" in profile:
                parts.append(f"  - Age: {profile['age']} years")
            
            if "bmi" in profile:
                parts.append(f"  - BMI: {profile['bmi']} ({profile.get('height', 'N/A')}, {profile.get('weight', 'N/A')})")
            
            if "blood_type" in profile:
                parts.append(f"  - Blood Type: {profile['blood_type']}")
            
            if profile.get("allergies"):
                allergies = ", ".join(profile["allergies"])
                parts.append(f"  - Allergies: {allergies}")
            
            if profile.get("chronic_conditions"):
                conditions = ", ".join(profile["chronic_conditions"])
                parts.append(f"  - Chronic Conditions: {conditions}")
            
            if profile.get("current_medications"):
                meds = ", ".join(profile["current_medications"])
                parts.append(f"  - Current Medications: {meds}")
            
            if "smoking_status" in profile:
                parts.append(f"  - Smoking Status: {profile['smoking_status']}")
            
            if "alcohol_consumption" in profile:
                parts.append(f"  - Alcohol: {profile['alcohol_consumption']}")
        
        # Recent history
        if "recent_history" in context and context["recent_history"]:
            parts.append("\nRecent Conversation:")
            for msg in context["recent_history"]:
                role_label = "Patient" if msg["role"] == "user" else "Assistant"
                parts.append(f"  {role_label}: {msg['content']}")
        
        return "\n".join(parts) if parts else "No additional medical context available."
    
    async def save_conversation_message(
        self,
        user_id: int,
        role: MessageRole,
        content: str,
        conversation_id: Optional[int] = None,
        ai_provider: Optional[str] = None,
        ai_model: Optional[str] = None,
        tokens_used: Optional[int] = None,
        context_snapshot: Optional[str] = None
    ) -> Message:
        """
        Save a message to conversation history
        Creates new conversation if none exists or if conversation_id not provided
        
        Args:
            user_id: User ID
            role: Message role (user/assistant/system)
            content: Message content
            conversation_id: Optional existing conversation ID
            ai_provider: AI provider used (openai, anthropic, etc.)
            ai_model: Model name
            tokens_used: Number of tokens used
            context_snapshot: JSON snapshot of context used
            
        Returns:
            Created Message object
        """
        # Get or create conversation
        if not conversation_id:
            # Try to get most recent active conversation
            conv_result = await self.db.execute(
                select(Conversation)
                .where(
                    Conversation.user_id == user_id,
                    Conversation.is_active == True
                )
                .order_by(desc(Conversation.updated_at))
                .limit(1)
            )
            conversation = conv_result.scalar_one_or_none()
            
            # Create new conversation if none exists or last one is old
            if not conversation:
                conversation = Conversation(
                    user_id=user_id,
                    title="Chat - " + datetime.utcnow().strftime("%Y-%m-%d %H:%M")
                )
                self.db.add(conversation)
                await self.db.flush()
            
            conversation_id = conversation.id
        
        # Create message
        message = Message(
            conversation_id=conversation_id,
            role=role,
            content=content,
            ai_provider=ai_provider,
            ai_model=ai_model,
            tokens_used=tokens_used,
            context_snapshot=context_snapshot
        )
        
        self.db.add(message)
        await self.db.commit()
        await self.db.refresh(message)
        
        return message
    
    async def create_conversation(
        self,
        user_id: int,
        title: Optional[str] = None
    ) -> Conversation:
        """
        Create a new conversation
        
        Args:
            user_id: User ID
            title: Optional conversation title
            
        Returns:
            Created Conversation object
        """
        conversation = Conversation(
            user_id=user_id,
            title=title or "New Conversation"
        )
        
        self.db.add(conversation)
        await self.db.commit()
        await self.db.refresh(conversation)
        
        return conversation


def get_medical_context_service(db: AsyncSession) -> MedicalContextService:
    """Factory function to get medical context service instance"""
    return MedicalContextService(db)
