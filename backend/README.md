# Medical AI Assistant - Backend

Professional REST API for an intelligent medical assistant.

## 📁 Project Structure

This backend follows a **modular, scalable architecture** with clear separation of concerns:

```
backend/
├── main.py              # Application entry point
├── config.py            # Configuration management
├── database.py          # Database connection
├── models/              # SQLAlchemy database models
├── schemas/             # Pydantic validation schemas
├── api/routes/          # API endpoints by domain
├── services/            # Business logic services
├── core/                # Application core (startup, etc.)
└── scripts/             # Utility scripts
```

📚 **See [STRUCTURE.md](STRUCTURE.md) for detailed architecture documentation**

## 🚀 Quick Start

### 1. Create virtual environment
```bash
python -m venv venv
```

### 2. Activate virtual environment
**Windows:**
```bash
.\venv\Scripts\activate
```

**Mac/Linux:**
```bash
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the server
```bash
uvicorn main:app --reload
```

## 📖 Documentation

Once the server is running:
- **API Docs (Swagger):** http://localhost:8000/docs
- **API Docs (ReDoc):** http://localhost:8000/redoc
- **Root endpoint:** http://localhost:8000

## 🧪 Test the API

### In your browser:
- http://localhost:8000/docs - Interactive documentation
- http://localhost:8000/health - API health status
- http://localhost:8000/info - Project information

### Test chat endpoint:
1. Open http://localhost:8000/docs
2. Click on POST /chat
3. Click "Try it out"
4. Enter:
   ```json
   {
     "text": "hello"
   }
   ```
5. Click "Execute"

## 📋 Available Endpoints

### System
- `GET /` - Welcome message
- `GET /health` - System health check
- `GET /info` - Project information and status
- `GET /stats` - System statistics
- `GET /hello/{name}` - Personalized greeting

### Users
- `POST /users/` - Create a new user
- `GET /users/` - List all users

### Appointments
- `POST /appointments/` - Create a new appointment
- `GET /appointments/` - List all appointments
- `GET /appointments/{id}` - Get specific appointment
- `DELETE /appointments/{id}` - Delete an appointment

### Chat
- `POST /chat/` - Chat with AI assistant

## 🛠️ Development Status

- ✅ **Phase 1**: Professional backend structure
- ✅ **Phase 2**: PostgreSQL database integration
- ✅ **Phase 3**: AI integration (LangChain + OpenAI/Anthropic)
- ✅ **Phase 4**: Code refactoring for scalability
- ✅ **Phase 5**: JWT Authentication system
- ⏳ **Phase 6**: WebSocket for real-time chat
- ⏳ **Phase 7**: Frontend with Next.js

**Current Progress: ~75%**

## 📚 Documentation

- [STRUCTURE.md](STRUCTURE.md) - Detailed architecture documentation
- [REFACTORING.md](REFACTORING.md) - Refactoring process and benefits
- [AUTHENTICATION.md](AUTHENTICATION.md) - JWT authentication guide
- [AI_SETUP.md](AI_SETUP.md) - AI configuration guide
- [SETUP.md](SETUP.md) - Initial setup instructions

## 🔧 Useful Commands

```bash
# Activate virtual environment
.\venv\Scripts\activate

# Run server
uvicorn main:app --reload

# Run on another port
uvicorn main:app --reload --port 8001

# Install new dependency
pip install package-name
pip freeze > requirements.txt
```

## 📝 Notes

- This is the learning backend phase 1
- No database yet
- No real AI yet
- Simple predefined responses
- All code in English (best practices)
