"""
LangGraph Agent Tools
Tools that the AI agent can use to perform actions
"""

from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta
from langchain.tools import tool
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_

from models import User, Appointment
from models.medical_profile import MedicalProfile
from models.medical_document import MedicalDocument
from services.vector_store_service import VectorStoreService
from services.document_processing_service import DocumentProcessingService


# Global references (will be set when tools are initialized)
_db_session: Optional[AsyncSession] = None
_vector_store: Optional[VectorStoreService] = None


def initialize_tools(db: AsyncSession):
    """Initialize tools with database session"""
    global _db_session, _vector_store
    _db_session = db
    _vector_store = VectorStoreService()


@tool
async def search_medical_documents(query: str, user_id: int, max_results: int = 3) -> str:
    """
    Search user's medical documents using semantic search.
    Useful for finding information in uploaded medical records, lab results, prescriptions, etc.
    
    Args:
        query: Search query text
        user_id: ID of the user
        max_results: Maximum number of results to return (default: 3)
    
    Returns:
        Formatted string with relevant document excerpts
    """
    if not _vector_store or not _vector_store.is_available():
        return "❌ Document search not available (OpenAI API key not configured)"
    
    try:
        context = await _vector_store.get_context_for_query(
            query=query,
            user_id=user_id,
            k=max_results
        )
        
        if not context:
            return "No relevant documents found for your query."
        
        return context
    except Exception as e:
        return f"❌ Error searching documents: {str(e)}"


@tool
async def get_user_medical_profile(user_id: int) -> str:
    """
    Get the user's complete medical profile.
    Useful for understanding patient's medical history and current health status.
    
    Args:
        user_id: ID of the user
    
    Returns:
        Formatted string with medical profile information
    """
    if not _db_session:
        return "❌ Database not available"
    
    try:
        # Get medical profile
        result = await _db_session.execute(
            select(MedicalProfile).where(MedicalProfile.user_id == user_id)
        )
        profile = result.scalar_one_or_none()
        
        if not profile:
            return "No medical profile found for this user."
        
        # Format output
        output = "=== MEDICAL PROFILE ===\n"
        
        # Basic info
        if profile.date_of_birth:
            from datetime import datetime
            age = (datetime.utcnow().date() - profile.date_of_birth).days // 365
            output += f"Age: {age} years\n"
        output += f"Blood Type: {profile.blood_type or 'Unknown'}\n"
        output += f"Height: {profile.height_cm}cm, Weight: {profile.weight_kg}kg\n"
        
        # Allergies
        if profile.allergies:
            output += f"\n⚠️ ALLERGIES:\n{profile.allergies}\n"
        
        # Chronic conditions
        if profile.chronic_conditions:
            output += f"\n🏥 CHRONIC CONDITIONS:\n{profile.chronic_conditions}\n"
        
        # Current medications
        if profile.current_medications:
            output += f"\n💊 CURRENT MEDICATIONS:\n{profile.current_medications}\n"
        
        # Past surgeries
        if profile.past_surgeries:
            output += f"\n🏥 PAST SURGERIES:\n{profile.past_surgeries}\n"
        
        # Lifestyle
        output += "\n📋 LIFESTYLE:\n"
        output += f"  - Smoking: {profile.smoking_status or 'Unknown'}\n"
        output += f"  - Alcohol: {profile.alcohol_consumption or 'Unknown'}\n"
        output += f"  - Exercise: {profile.exercise_frequency or 'Unknown'}\n"
        
        return output
        
    except Exception as e:
        return f"❌ Error fetching medical profile: {str(e)}"


@tool
async def get_upcoming_appointments(user_id: int, days_ahead: int = 30) -> str:
    """
    Get user's upcoming appointments.
    
    Args:
        user_id: ID of the user
        days_ahead: Number of days to look ahead (default: 30)
    
    Returns:
        Formatted string with upcoming appointments
    """
    if not _db_session:
        return "❌ Database not available"
    
    try:
        now = datetime.utcnow()
        future_date = now + timedelta(days=days_ahead)
        
        result = await _db_session.execute(
            select(Appointment).where(
                and_(
                    Appointment.user_id == user_id,
                    Appointment.appointment_date >= now,
                    Appointment.appointment_date <= future_date
                )
            ).order_by(Appointment.appointment_date)
        )
        appointments = result.scalars().all()
        
        if not appointments:
            return f"No upcoming appointments in the next {days_ahead} days."
        
        output = f"=== UPCOMING APPOINTMENTS ({len(appointments)}) ===\n"
        for apt in appointments:
            output += f"\n📅 {apt.appointment_date.strftime('%Y-%m-%d %H:%M')}\n"
            output += f"   Type: {apt.appointment_type}\n"
            output += f"   Doctor: {apt.doctor_name}\n"
            if apt.reason:
                output += f"   Reason: {apt.reason}\n"
            output += f"   Status: {apt.status}\n"
        
        return output
        
    except Exception as e:
        return f"❌ Error fetching appointments: {str(e)}"


@tool
async def create_appointment(
    user_id: int,
    appointment_date: str,
    appointment_type: str,
    doctor_name: str,
    reason: Optional[str] = None
) -> str:
    """
    Create a new appointment for the user.
    
    Args:
        user_id: ID of the user
        appointment_date: Date and time in ISO format (e.g., "2026-02-15T10:00:00")
        appointment_type: Type of appointment (e.g., "General Checkup", "Follow-up", "Specialist")
        doctor_name: Name of the doctor
        reason: Optional reason for the appointment
    
    Returns:
        Confirmation message
    """
    if not _db_session:
        return "❌ Database not available"
    
    try:
        # Parse date
        try:
            apt_date = datetime.fromisoformat(appointment_date.replace('Z', '+00:00'))
        except ValueError:
            return f"❌ Invalid date format. Use ISO format like '2026-02-15T10:00:00'"
        
        # Check if date is in the future
        if apt_date < datetime.utcnow():
            return "❌ Cannot create appointment in the past"
        
        # Create appointment
        appointment = Appointment(
            user_id=user_id,
            appointment_date=apt_date,
            appointment_type=appointment_type,
            doctor_name=doctor_name,
            reason=reason,
            status="scheduled"
        )
        
        _db_session.add(appointment)
        await _db_session.commit()
        await _db_session.refresh(appointment)
        
        return f"✅ Appointment created successfully!\n" \
               f"📅 Date: {apt_date.strftime('%Y-%m-%d %H:%M')}\n" \
               f"👨‍⚕️ Doctor: {doctor_name}\n" \
               f"📋 Type: {appointment_type}\n" \
               f"ID: {appointment.id}"
        
    except Exception as e:
        await _db_session.rollback()
        return f"❌ Error creating appointment: {str(e)}"


@tool
async def list_medical_documents(user_id: int, limit: int = 10) -> str:
    """
    List user's uploaded medical documents.
    
    Args:
        user_id: ID of the user
        limit: Maximum number of documents to return (default: 10)
    
    Returns:
        Formatted list of documents
    """
    if not _db_session:
        return "❌ Database not available"
    
    try:
        result = await _db_session.execute(
            select(MedicalDocument)
            .where(MedicalDocument.user_id == user_id)
            .order_by(MedicalDocument.created_at.desc())
            .limit(limit)
        )
        documents = result.scalars().all()
        
        if not documents:
            return "No medical documents found."
        
        output = f"=== MEDICAL DOCUMENTS ({len(documents)}) ===\n"
        for doc in documents:
            output += f"\n📄 {doc.title or doc.filename or 'Untitled'}\n"
            output += f"   Type: {doc.document_type}\n"
            output += f"   Uploaded: {doc.created_at.strftime('%Y-%m-%d')}\n"
            output += f"   Status: {doc.processing_status}\n"
            if doc.description:
                output += f"   Description: {doc.description}\n"
        
        return output
        
    except Exception as e:
        return f"❌ Error listing documents: {str(e)}"


@tool
def get_current_date_time() -> str:
    """
    Get the current date and time.
    Useful for scheduling appointments or understanding temporal context.
    
    Returns:
        Current date and time in readable format
    """
    now = datetime.utcnow()
    return f"Current date and time: {now.strftime('%Y-%m-%d %H:%M:%S UTC')}\n" \
           f"Today is {now.strftime('%A, %B %d, %Y')}"


# Export all tools
AGENT_TOOLS = [
    search_medical_documents,
    get_user_medical_profile,
    get_upcoming_appointments,
    create_appointment,
    list_medical_documents,
    get_current_date_time
]
