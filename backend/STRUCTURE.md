# 📁 Project Structure - Medical AI Assistant

## Directory Organization

```
backend/
│
├── 📄 main.py                    # FastAPI application entry point
├── 📄 config.py                  # Centralized configuration
├── 📄 database.py                # Database connection setup
│
├── 📂 models/                    # SQLAlchemy database models
│   ├── __init__.py              # Model exports
│   ├── base.py                  # Declarative base
│   ├── user.py                  # User model
│   └── appointment.py           # Appointment model
│
├── 📂 schemas/                   # Pydantic validation schemas
│   ├── __init__.py              # Schema exports
│   ├── user.py                  # User schemas (Create/Read)
│   ├── appointment.py           # Appointment schemas
│   └── chat.py                  # Chat schemas
│
├── 📂 api/                       # API layer
│   ├── __init__.py              # API exports
│   ├── deps.py                  # Shared dependencies (get_db)
│   └── routes/                  # API endpoints by domain
│       ├── __init__.py
│       ├── users.py             # User CRUD endpoints
│       ├── appointments.py      # Appointment CRUD endpoints
│       ├── chat.py              # AI chat endpoint
│       └── system.py            # Health, info, stats endpoints
│
├── 📂 services/                  # Business logic services
│   ├── __init__.py
│   └── chat_service.py          # AI chat service (LangChain)
│
├── 📂 core/                      # Application core
│   ├── __init__.py
│   └── startup.py               # Lifecycle management
│
├── 📂 scripts/                   # Utility scripts
│   └── init_db.py               # Database initialization
│
├── 📄 requirements.txt           # Python dependencies
├── 📄 .env.example              # Environment variables template
└── 📄 README.md                 # This file
```

## 🏗️ Architecture Layers

### 1. **Entry Point Layer**
- `main.py`: Application initialization, middleware, router registration

### 2. **API Layer** (`api/`)
- **Routes**: HTTP endpoints organized by domain
- **Dependencies**: Shared utilities like database sessions

### 3. **Schema Layer** (`schemas/`)
- **Request/Response Models**: Pydantic models for validation
- Type-safe data contracts between client and server

### 4. **Service Layer** (`services/`)
- **Business Logic**: Complex operations, external service integrations
- **AI Services**: LangChain integration, chat logic

### 5. **Data Layer** (`models/`)
- **ORM Models**: SQLAlchemy models mapping to database tables
- Database schema definitions

### 6. **Core Layer** (`core/`)
- **Configuration**: Application settings
- **Lifecycle**: Startup/shutdown handlers

## 📊 Data Flow

```
HTTP Request
    ↓
[API Route]  ← Uses schemas for validation
    ↓
[Service]    ← Business logic
    ↓
[Model]      ← Database operations
    ↓
Database (PostgreSQL)
```

## 🔄 Request Lifecycle Example

### Creating a User
1. **Client** sends POST to `/users/`
2. **Router** (`api/routes/users.py`) receives request
3. **Schema** (`schemas/user.py`) validates UserCreate data
4. **Dependency** (`api/deps.py`) provides database session
5. **Model** (`models/user.py`) creates User instance
6. **Database** saves user via SQLAlchemy
7. **Schema** (`schemas/user.py`) formats UserRead response
8. **Router** returns response to client

### Chat with AI
1. **Client** sends POST to `/chat/`
2. **Router** (`api/routes/chat.py`) receives request
3. **Schema** (`schemas/chat.py`) validates ChatRequest
4. **Service** (`services/chat_service.py`) processes with LangChain
5. **AI Provider** (OpenAI/Anthropic) generates response
6. **Schema** formats ChatResponse
7. **Router** returns response

## 🎯 Module Responsibilities

### `main.py`
- Create FastAPI app
- Configure middleware (CORS)
- Register routers
- Define lifespan

### `config.py`
- Environment variables
- Application settings
- Configuration validation

### `database.py`
- Database URL
- Engine creation
- Session management

### `models/*.py`
- Database table definitions
- Relationships
- Database constraints

### `schemas/*.py`
- Request validation
- Response serialization
- Data transfer objects

### `api/routes/*.py`
- HTTP endpoint definitions
- Request handling
- Response formatting
- Error handling

### `services/*.py`
- Business logic
- External service integration
- Complex operations
- Data transformations

### `core/*.py`
- Application lifecycle
- Startup initialization
- Shutdown cleanup

## 🔧 Key Design Patterns

### Dependency Injection
```python
# api/deps.py
async def get_db() -> AsyncSession:
    async with SessionLocal() as session:
        yield session

# api/routes/users.py
@router.post("/")
async def create_user(
    user: UserCreate,
    db: AsyncSession = Depends(get_db)  # ← Injected
):
    ...
```

### Service Layer Pattern
```python
# services/chat_service.py
class ChatService:
    async def chat(self, message: str) -> str:
        # Complex business logic here
        ...

# api/routes/chat.py
@router.post("/")
async def chat(message: ChatRequest):
    service = get_chat_service()  # ← Service
    response = await service.chat(message.text)
    ...
```

### Repository Pattern (Implicit with SQLAlchemy)
```python
# models/user.py
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    ...

# api/routes/users.py
result = await db.execute(select(User))  # ← Repository-like
users = result.scalars().all()
```

## 📝 Naming Conventions

### Files
- `snake_case.py` for all Python files
- Singular for models: `user.py`, `appointment.py`
- Plural for collections: `users.py` (routes), `models/` (folder)

### Classes
- `PascalCase` for classes
- Descriptive names: `ChatService`, `UserCreate`

### Functions
- `snake_case` for functions
- Verb-noun pattern: `create_user()`, `get_appointment()`

### Routes
- Plural nouns: `/users/`, `/appointments/`
- RESTful conventions: GET, POST, PUT, DELETE

## 🚀 Adding New Features

### Add a New Model
1. Create `models/new_model.py`
2. Define SQLAlchemy model
3. Export in `models/__init__.py`
4. Create migration/update schema

### Add a New Endpoint
1. Create schemas in `schemas/new_feature.py`
2. Create router in `api/routes/new_feature.py`
3. Register router in `main.py`

### Add a New Service
1. Create `services/new_service.py`
2. Define service class
3. Export in `services/__init__.py`
4. Use in routes

## 📚 Import Examples

```python
# Models
from models import User, Appointment, Base

# Schemas
from schemas.user import UserCreate, UserRead
from schemas.appointment import AppointmentCreate, AppointmentRead

# Services
from services.chat_service import get_chat_service

# Dependencies
from api.deps import get_db

# Core
from core import lifespan
from config import settings
```

## 🔍 Finding Things

- **Need to add endpoint?** → `api/routes/`
- **Need to modify data structure?** → `models/` (database) or `schemas/` (API)
- **Need to add business logic?** → `services/`
- **Need to configure something?** → `config.py`
- **Need to modify startup?** → `core/startup.py`
- **Need to see all endpoints?** → `main.py` (router registration)

---

*This structure follows industry best practices for FastAPI applications and scales from small projects to enterprise applications.*
