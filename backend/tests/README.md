# Test Configuration

## Running Tests

### Install Test Dependencies
```bash
pip install pytest pytest-asyncio httpx websockets
```

### Run All Tests
```bash
# From backend directory
pytest

# With verbose output
pytest -v

# With coverage
pytest --cov=. --cov-report=html
```

### Run Specific Test Categories
```bash
# Unit tests only (fast)
pytest tests/unit/ -v

# Integration tests only
pytest tests/integration/ -v

# E2E tests only
pytest tests/e2e/ -v

# Skip slow tests
pytest -m "not slow"

# Run only agent tests
pytest tests/integration/test_agent_api.py -v
```

### Run Tests with Markers
```bash
# Run only unit tests
pytest -m unit

# Run only integration tests
pytest -m integration

# Run only e2e tests
pytest -m e2e

# Skip slow tests
pytest -m "not slow"
```

## Test Structure

```
tests/
├── conftest.py              # Shared fixtures and configuration
├── unit/                    # Unit tests (fast, isolated)
│   ├── test_models.py
│   ├── test_services.py
│   └── test_utils.py
├── integration/             # Integration tests (API + DB)
│   ├── test_auth_api.py
│   ├── test_agent_api.py
│   ├── test_chat_api.py
│   └── test_websocket.py
├── e2e/                     # End-to-end tests (full flows)
│   └── test_user_flow.py
└── fixtures/                # Test data and helpers
    ├── test_data.py
    └── factories.py
```

## Test Database

Tests use a separate test database to avoid affecting development data.

### Setup Test Database
```bash
# Set environment variable
export TEST_DATABASE_URL="postgresql+asyncpg://postgres:postgres@localhost:5433/medical_test"

# Or add to .env.test
TEST_DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5433/medical_test
```

### Create Test Database
```sql
CREATE DATABASE medical_test;
```

## Fixtures

### Common Fixtures (from conftest.py)

- `db_session`: Fresh database session for each test
- `clean_db`: Clean database state
- `test_user`: Pre-created test user
- `authenticated_user`: User with auth token
- `api_headers`: Headers with authentication
- `password_context`: Password hashing context

### Usage Example
```python
@pytest.mark.asyncio
async def test_example(db_session, test_user, api_headers):
    # db_session: database connection
    # test_user: existing user object
    # api_headers: {"Authorization": "Bearer token"}
    pass
```

## Writing Tests

### Unit Test Example
```python
# tests/unit/test_services.py
import pytest
from services.chat_service import ChatService

pytestmark = pytest.mark.unit

class TestChatService:
    def test_build_prompt(self):
        service = ChatService()
        prompt = service._build_system_prompt(context="Test context")
        assert "Test context" in prompt
```

### Integration Test Example
```python
# tests/integration/test_api.py
import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.integration

@pytest.mark.asyncio
async def test_endpoint(async_client: AsyncClient, api_headers):
    response = await async_client.get("/endpoint", headers=api_headers)
    assert response.status_code == 200
```

### E2E Test Example
```python
# tests/e2e/test_flow.py
import pytest

pytestmark = pytest.mark.e2e

@pytest.mark.asyncio
async def test_complete_user_flow(async_client):
    # 1. Register
    # 2. Login
    # 3. Create profile
    # 4. Use service
    pass
```

## Continuous Integration

### GitHub Actions Example
```yaml
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
      - run: pip install -r requirements.txt
      - run: pytest tests/unit  # Fast tests
      - run: pytest tests/integration  # Slower tests
```

## Best Practices

1. **Isolate tests**: Each test should be independent
2. **Use fixtures**: Reuse common setup with pytest fixtures
3. **Fast unit tests**: Keep unit tests under 1 second
4. **Mark slow tests**: Use `@pytest.mark.slow` for integration tests
5. **Clean database**: Use transactions that rollback after tests
6. **Mock external APIs**: Don't call real AI APIs in tests
7. **Test edge cases**: Include error scenarios
8. **Descriptive names**: Use clear test function names
9. **AAA pattern**: Arrange, Act, Assert

## Troubleshooting

### Tests fail with database errors
```bash
# Reset test database
python scripts/init_db.py --test
```

### Tests timeout
```bash
# Increase timeout for slow tests
pytest --timeout=300
```

### Import errors
```bash
# Ensure PYTHONPATH includes backend
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```
