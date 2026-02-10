# Testing Guide

## Overview

This project uses **pytest** for testing with a well-organized structure separating unit, integration, and end-to-end tests.

## Quick Start

### 1. Install Test Dependencies

```bash
pip install pytest pytest-asyncio httpx websockets
```

### 2. Setup Test Database

Create a separate PostgreSQL database for testing:

```sql
CREATE DATABASE medical_test;
```

Configure test database URL:
```bash
# .env or export
export TEST_DATABASE_URL="postgresql+asyncpg://postgres:postgres@localhost:5433/medical_test"
```

### 3. Run Tests

```bash
# All tests
pytest

# Specific category
pytest tests/unit        # Unit tests only
pytest tests/integration # Integration tests
pytest -m unit           # Using markers

# Verbose output
pytest -v

# With coverage
pytest --cov=. --cov-report=html
```

## Test Organization

### Directory Structure

```
tests/
├── conftest.py              # Shared fixtures
├── unit/                    # Unit tests (isolated, fast)
│   ├── test_models.py       # Model tests
│   ├── test_services.py     # Service logic tests
│   └── test_utils.py        # Utility function tests
├── integration/             # Integration tests (API + DB)
│   ├── test_auth_api.py     # Authentication endpoints
│   ├── test_agent_api.py    # Agent/chat endpoints
│   ├── test_chat_api.py     # Chat service tests
│   └── test_websocket.py    # WebSocket connection tests
├── e2e/                     # End-to-end tests (full flows)
│   └── test_user_flow.py    # Complete user journeys
└── fixtures/                # Test data and helpers
    └── test_data.py         # Sample medical data
```

### Test Categories

#### Unit Tests (`tests/unit/`)
- **Purpose**: Test individual components in isolation
- **Characteristics**: Fast, no external dependencies, mocked
- **Run**: `pytest tests/unit` or `pytest -m unit`
- **Example**: Testing model methods, utility functions

#### Integration Tests (`tests/integration/`)
- **Purpose**: Test API endpoints with real database
- **Characteristics**: Slower, uses test database, HTTP requests
- **Run**: `pytest tests/integration` or `pytest -m integration`
- **Example**: Testing REST endpoints, WebSocket connections

#### E2E Tests (`tests/e2e/`)
- **Purpose**: Test complete user workflows
- **Characteristics**: Slowest, full system interaction
- **Run**: `pytest tests/e2e` or `pytest -m e2e`
- **Example**: Register → Login → Upload Document → Chat

## Fixtures (conftest.py)

### Database Fixtures

```python
# Fresh database session (auto-rollback)
async def test_example(db_session):
    user = User(name="Test")
    db_session.add(user)
    await db_session.commit()
    # Changes rolled back after test
```

```python
# Clean database (drop all)
async def test_example(clean_db, db_session):
    # Start with empty database
    pass
```

### User Fixtures

```python
# Basic test user
async def test_example(test_user):
    assert test_user.email == "test@example.com"
```

```python
# User with medical profile
async def test_example(test_user_with_profile):
    assert test_user_with_profile.medical_profile is not None
```

```python
# User with appointments
async def test_example(test_user_with_appointments):
    # User has 2 upcoming appointments
    pass
```

```python
# User with documents
async def test_example(test_user_with_documents):
    # User has lab results and prescription
    pass
```

### Authentication Fixtures

```python
# Authenticated user (tuple)
async def test_example(authenticated_user):
    user, token = authenticated_user
    # Use token for API calls
```

```python
# API headers with auth token
async def test_example(async_client, api_headers):
    response = await async_client.get("/endpoint", headers=api_headers)
```

### HTTP Client Fixtures

```python
# Async HTTP client (for FastAPI)
async def test_example(async_client):
    response = await async_client.post("/auth/login", json={...})
    assert response.status_code == 200
```

```python
# WebSocket client
async def test_example(websocket_client):
    async with websocket_client as ws:
        await ws.send_json({"message": "Hello"})
        response = await ws.receive_json()
```

## Writing Tests

### Test Class Pattern

```python
import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.integration  # Mark all tests in file

class TestAuthentication:
    """Test authentication endpoints"""
    
    @pytest.mark.asyncio
    async def test_register(self, async_client):
        """Test user registration"""
        response = await async_client.post("/auth/register", json={
            "name": "New User",
            "email": "new@example.com",
            "password": "SecurePass123!"
        })
        
        assert response.status_code == 201
        assert "id" in response.json()
    
    @pytest.mark.asyncio
    async def test_login(self, async_client, test_user):
        """Test user login"""
        response = await async_client.post("/auth/login", data={
            "username": test_user.email,
            "password": "testpass123"
        })
        
        assert response.status_code == 200
        assert "access_token" in response.json()
```

### Using Markers

```python
@pytest.mark.unit
def test_fast():
    """Unit test - fast"""
    pass

@pytest.mark.integration
async def test_api():
    """Integration test - database + API"""
    pass

@pytest.mark.slow
async def test_long_running():
    """Slow test - mark to skip in CI"""
    pass
```

Run specific markers:
```bash
pytest -m unit          # Only unit tests
pytest -m "not slow"    # Skip slow tests
```

## Best Practices

### 1. Test Independence
Each test should work independently:
- Use fixtures for setup
- Don't rely on test execution order
- Database changes are rolled back automatically

### 2. Clear Test Names
```python
# Good
async def test_user_cannot_login_with_wrong_password():
    pass

# Bad
async def test_login_fail():
    pass
```

### 3. AAA Pattern
- **Arrange**: Setup test data
- **Act**: Execute the action
- **Assert**: Verify the outcome

```python
async def test_example(async_client):
    # Arrange
    user_data = {"name": "Test", "email": "test@example.com"}
    
    # Act
    response = await async_client.post("/users", json=user_data)
    
    # Assert
    assert response.status_code == 201
```

### 4. Test Edge Cases
Don't just test happy paths:
- Invalid input
- Missing fields
- Unauthorized access
- Edge cases (empty strings, null, etc.)

### 5. Mock External Services
```python
from unittest.mock import patch

@pytest.mark.asyncio
async def test_with_mock(async_client):
    with patch('services.openai_service.call_api') as mock:
        mock.return_value = {"response": "Mocked"}
        # Test your code without calling real API
```

## Running Tests in CI/CD

### GitHub Actions Example

```yaml
name: Tests
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: postgres
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
    
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install pytest pytest-asyncio httpx
      
      - name: Run unit tests
        run: pytest tests/unit -v
      
      - name: Run integration tests
        run: pytest tests/integration -v
        env:
          TEST_DATABASE_URL: postgresql+asyncpg://postgres:postgres@localhost:5432/test
```

## Troubleshooting

### Database Connection Errors

```bash
# Verify test database exists
psql -U postgres -c "CREATE DATABASE medical_test;"

# Check connection string
echo $TEST_DATABASE_URL
```

### Import Errors

```bash
# Add backend to PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)/backend"
```

### Slow Tests

```bash
# Skip slow tests
pytest -m "not slow"

# Increase timeout
pytest --timeout=300
```

### Fixture Scope Issues

If you see "function scope fixture used in session scope":
- Change fixture scope: `@pytest.fixture(scope="session")`
- Or restructure dependencies

## Test Data

Sample test data is available in `tests/fixtures/test_data.py`:

```python
from tests.fixtures.test_data import (
    SAMPLE_MEDICAL_PROFILE,
    SAMPLE_APPOINTMENTS,
    SAMPLE_DOCUMENTS
)
```

## Coverage

Generate coverage report:

```bash
# HTML report
pytest --cov=. --cov-report=html
open htmlcov/index.html

# Terminal report
pytest --cov=. --cov-report=term

# Minimum coverage threshold
pytest --cov=. --cov-fail-under=80
```

## Next Steps

1. **Add more unit tests**: Test individual service functions
2. **E2E tests**: Complete user workflows
3. **Performance tests**: Load testing for API
4. **Security tests**: Test authentication edge cases
5. **Mock AI services**: Avoid calling real APIs in tests

## Resources

- [Pytest Documentation](https://docs.pytest.org/)
- [pytest-asyncio](https://pypi.org/project/pytest-asyncio/)
- [FastAPI Testing](https://fastapi.tiangolo.com/tutorial/testing/)
