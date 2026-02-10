"""
Pytest configuration and shared fixtures
"""
import pytest  # type: ignore
import asyncio
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from passlib.context import CryptContext
from datetime import datetime, timedelta
import os
import sys
from pathlib import Path
from httpx import AsyncClient, ASGITransport

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from database import Base, get_db
from models import User, MedicalProfile, BloodType, Appointment, MedicalDocument, DocumentType
from main import app


# Pytest configuration
def pytest_configure(config):
    """Configure pytest"""
    config.addinivalue_line(
        "markers", "unit: Unit tests (fast, no external dependencies)"
    )
    config.addinivalue_line(
        "markers", "integration: Integration tests (API + DB)"
    )
    config.addinivalue_line(
        "markers", "e2e: End-to-end tests (full user flows)"
    )
    config.addinivalue_line(
        "markers", "slow: Tests that take significant time"
    )


# Event loop fixture for async tests
@pytest.fixture(scope="session")
def event_loop():
    """Create event loop for async tests"""
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


# Test Database Engine (session-scoped)
@pytest.fixture(scope="session")
async def test_engine():
    """Create test database engine"""
    test_db_url = os.getenv(
        "TEST_DATABASE_URL",
        "postgresql+asyncpg://postgres:postgres@localhost:5433/medical_test"
    )
    
    engine = create_async_engine(test_db_url, echo=False, pool_pre_ping=True)
    
    # Create all tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    
    yield engine
    
    # Cleanup
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    
    await engine.dispose()


# Database session (function-scoped)
@pytest.fixture
async def db_session(test_engine) -> AsyncGenerator[AsyncSession, None]:
    """
    Create a fresh database session for each test
    Automatically rolls back changes after test
    """
    async_session_factory = async_sessionmaker(
        test_engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autoflush=False,
        autocommit=False
    )
    
    async with async_session_factory() as session:
        async with session.begin():
            yield session
            await session.rollback()


@pytest.fixture
async def clean_db(test_engine):
    """
    Clean database before test
    Use this when you need a completely fresh database
    """
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield
    # Tables recreated each session, no need to drop again


# Password hashing
@pytest.fixture
def password_context():
    """Password hashing context"""
    return CryptContext(schemes=["bcrypt"], deprecated="auto")


# User fixtures
@pytest.fixture
async def test_user(db_session: AsyncSession, password_context):
    """
    Create a basic test user
    Returns: User object
    """
    user = User(
        name="Test User",
        email="test@example.com",
        password_hash=password_context.hash("testpass123"),
        is_active=True,
        created_at=datetime.utcnow()
    )
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    return user


@pytest.fixture
async def test_user_with_profile(db_session: AsyncSession, test_user):
    """
    Create test user with complete medical profile
    Returns: User object (with profile relationship loaded)
    """
    profile = MedicalProfile(
        user_id=test_user.id,
        blood_type=BloodType.O_POSITIVE,
        height_cm=175,
        weight_kg=75,
        date_of_birth=datetime(1985, 3, 15),
        allergies=["Penicillin (moderate rash)", "Peanuts (anaphylaxis)"],
        chronic_conditions=["Type 2 Diabetes", "Hypertension"],
        current_medications=[
            {"name": "Metformin", "dosage": "500mg", "frequency": "twice daily"},
            {"name": "Lisinopril", "dosage": "10mg", "frequency": "once daily"}
        ],
        past_surgeries=[{"name": "Appendectomy", "date": "2010"}],
        smoking_status="former",
        alcohol_consumption="occasional",
        exercise_frequency="moderate"
    )
    
    db_session.add(profile)
    await db_session.commit()
    await db_session.refresh(test_user)
    
    return test_user


@pytest.fixture
async def test_user_with_appointments(db_session: AsyncSession, test_user):
    """
    Create test user with upcoming appointments
    Returns: User object
    """
    appointments = [
        Appointment(
            user_id=test_user.id,
            description=f"Cardiology - Dr. Smith - {(datetime.utcnow() + timedelta(days=7)).strftime('%Y-%m-%d')} - Regular checkup"
        ),
        Appointment(
            user_id=test_user.id,
            description=f"Lab Test - {(datetime.utcnow() + timedelta(days=14)).strftime('%Y-%m-%d')} - Blood work"
        )
    ]
    
    for apt in appointments:
        db_session.add(apt)
    
    await db_session.commit()
    return test_user


@pytest.fixture
async def test_user_with_documents(db_session: AsyncSession, test_user):
    """
    Create test user with medical documents
    Returns: User object
    """
    documents = [
        MedicalDocument(
            user_id=test_user.id,
            title="Lab Results - Blood Work",
            file_name="lab_results_2024.pdf",
            file_path="/uploads/test/lab_results_2024.pdf",
            mime_type="application/pdf",
            document_type=DocumentType.LAB_RESULT,
            description="Complete blood count and metabolic panel",
            extracted_text="Glucose: 105 mg/dL (slightly elevated)\nHemoglobin: 14.5 g/dL (normal)"
        ),
        MedicalDocument(
            user_id=test_user.id,
            title="Prescription Record",
            file_name="prescription_2024.pdf",
            file_path="/uploads/test/prescription_2024.pdf",
            mime_type="application/pdf",
            document_type=DocumentType.PRESCRIPTION,
            description="Current medication prescriptions",
            extracted_text="Metformin 500mg - twice daily\nLisinopril 10mg - once daily"
        )
    ]
    
    for doc in documents:
        db_session.add(doc)
    
    await db_session.commit()
    return test_user


# Authentication fixtures
@pytest.fixture
async def authenticated_user(test_user):
    """
    Get authenticated user with JWT token
    Returns: tuple (user, token)
    """
    from core.security import create_access_token  # type: ignore
    
    token_data = {"sub": test_user.email}
    token = create_access_token(token_data)
    
    return test_user, token


@pytest.fixture
def api_headers(authenticated_user):
    """
    Get headers with authentication token
    Usage: client.get("/endpoint", headers=api_headers)
    """
    _, token = authenticated_user
    return {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }


# HTTP Client fixtures
@pytest.fixture
async def async_client(test_engine) -> AsyncGenerator[AsyncClient, None]:
    """
    Provide async HTTP client for API testing
    Automatically overrides database dependency
    """
    # Override database dependency to use test database
    async def override_get_db():
        async_session_factory = async_sessionmaker(
            test_engine,
            class_=AsyncSession,
            expire_on_commit=False
        )
        async with async_session_factory() as session:
            yield session
    
    app.dependency_overrides[get_db] = override_get_db
    
    # Create async client
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
        timeout=30.0
    ) as client:
        yield client
    
    # Clear overrides
    app.dependency_overrides.clear()


@pytest.fixture
def websocket_client(authenticated_user):
    """
    Provide WebSocket client for testing
    Returns: TestClient with websocket_connect method
    """
    from fastapi.testclient import TestClient
    
    _, token = authenticated_user
    client = TestClient(app)
    
    # Return WebSocket connection context
    return client.websocket_connect(f"/ws/chat?token={token}")


# Environment fixtures
@pytest.fixture(scope="session", autouse=True)
def setup_test_env():
    """
    Setup test environment variables
    Runs once per test session
    """
    os.environ["TESTING"] = "1"
    os.environ["TEST_DATABASE_URL"] = os.getenv(
        "TEST_DATABASE_URL",
        "postgresql+asyncpg://postgres:postgres@localhost:5433/medical_test"
    )
    yield
    # Cleanup
    if "TESTING" in os.environ:
        del os.environ["TESTING"]
