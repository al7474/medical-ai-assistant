"""
Unit Tests for Models
Tests: User, MedicalProfile, Appointment, etc.
"""
import pytest  # type: ignore
from datetime import datetime
from models import User, MedicalProfile, BloodType, Appointment
from sqlalchemy.ext.asyncio import AsyncSession

pytestmark = pytest.mark.unit


class TestUserModel:
    """Test User model"""
    
    @pytest.mark.asyncio
    async def test_create_user(self, db_session: AsyncSession, password_context):
        """Test creating a user"""
        user = User(
            name="Test User",
            email="test@example.com",
            password_hash=password_context.hash("testpass"),
            is_active=True
        )
        
        db_session.add(user)
        await db_session.commit()
        await db_session.refresh(user)
        
        assert user.id is not None
        assert user.email == "test@example.com"
        assert user.is_active is True
    
    @pytest.mark.asyncio
    async def test_user_email_unique(self, db_session: AsyncSession, test_user):
        """Test email uniqueness constraint"""
        duplicate_user = User(
            name="Another User",
            email=test_user.email,  # Same email
            password_hash="hash123",
            is_active=True
        )
        
        db_session.add(duplicate_user)
        
        with pytest.raises(Exception):  # Should raise integrity error
            await db_session.commit()


class TestMedicalProfileModel:
    """Test MedicalProfile model"""
    
    @pytest.mark.asyncio
    async def test_create_medical_profile(self, db_session: AsyncSession, test_user):
        """Test creating medical profile"""
        profile = MedicalProfile(
            user_id=test_user.id,
            blood_type=BloodType.O_POSITIVE,
            height_cm=175,
            weight_kg=70,
            date_of_birth=datetime(1990, 1, 1),
            allergies=["Penicillin"],
            chronic_conditions=["Diabetes"],
            smoking_status="never"
        )
        
        db_session.add(profile)
        await db_session.commit()
        await db_session.refresh(profile)
        
        assert profile.id is not None
        assert profile.user_id == test_user.id
        assert profile.blood_type == BloodType.O_POSITIVE
        assert len(profile.allergies) == 1
    
    @pytest.mark.asyncio
    async def test_profile_to_context_dict(self, db_session: AsyncSession, test_user):
        """Test profile context dictionary conversion"""
        profile = MedicalProfile(
            user_id=test_user.id,
            blood_type=BloodType.A_POSITIVE,
            height_cm=180,
            weight_kg=75,
            date_of_birth=datetime(1985, 6, 15),
            allergies=["Peanuts", "Shellfish"]
        )
        
        context = profile.to_context_dict()
        
        assert "blood_type" in context
        assert "bmi" in context
        assert "age" in context
        assert "allergies" in context
        assert context["blood_type"] == "A+"


class TestAppointmentModel:
    """Test Appointment model"""
    
    @pytest.mark.asyncio
    async def test_create_appointment(self, db_session: AsyncSession, test_user):
        """Test creating an appointment"""
        appointment = Appointment(
            user_id=test_user.id,
            description="Doctor visit - 2026-03-01 at 10:00 AM"
        )
        
        db_session.add(appointment)
        await db_session.commit()
        await db_session.refresh(appointment)
        
        assert appointment.id is not None
        assert appointment.user_id == test_user.id
        assert "Doctor visit" in appointment.description
