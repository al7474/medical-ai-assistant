# 🏥 Medical AI Assistant

Intelligent medical assistant that converses with patients, understands their needs, and manages appointments and documents automatically.

## 🎯 Project Vision

An AI-powered medical assistant that:
- 💬 Converses naturally with patients
- 🤖 Understands intentions and context
- 📅 Manages appointments automatically
- 📄 Handles medical documents
- 🔒 Secure and reliable

## 🛠️ Tech Stack

| Component | Technology | Status |
|-----------|------------|--------|
| Frontend | Next.js 14 + TypeScript | ✅ Phase 7 complete |
| Backend | FastAPI | ✅ Phase 6 complete |
| Database | PostgreSQL | ✅ Running (port 5433) |
| AI | LangChain + LLM | ✅ Configured (requires API key) |
| Authentication | JWT | ✅ Complete |
| WebSocket | FastAPI WS | ✅ Real-time chat working |
| Cache | Redis | ⏳ Future phase |
| Containers | Docker | ✅ PostgreSQL in Docker |

## 🚀 Current Status: Phase 7 - Complete Frontend ✅

### ✅ Completed
- REST API working with FastAPI
- **Automatic database initialization**
- Complete CRUD endpoints (users, appointments)
- PostgreSQL with Docker (port 5433)
- **Statistics system**
- **AI Chat Service with LangChain** 🤖✨
- **Support for OpenAI GPT and Anthropic Claude**
- **Intelligent fallback without API key**
- **Complete JWT Authentication System** 🔐
  - User registration with validation
  - Login with JWT tokens
  - Protected routes
  - Password hashing with bcrypt
- **WebSocket for real-time chat** 🌐✨
  - JWT-authenticated connections
  - Multiple simultaneous users support
  - Typing indicators
  - AI integration
  - Interactive HTML test client
- **Complete Next.js 14 Frontend** 💎✨
  - Modern interface with Tailwind CSS
  - Login and registration pages
  - Dashboard with real-time chat
  - Complete WebSocket integration
  - State management with Zustand
  - Fully typed with TypeScript
- Automatic documentation
- Project structure ready
- No Pydantic warnings
### 🚧 Next Steps
- **Advanced Features**: Chat history, notifications, user roles
- **Production Deployment**: Docker, CI/CD, monitoring

## 📁 Project Structure

```
medical-ai-assistant/
├── backend/             ✅ Complete
│   ├── main.py          # FastAPI application
│   ├── models/          # Database models
│   ├── database.py      # PostgreSQL connection
│   ├── services/        # Business logic
│   ├── api/routes/      # API endpoints
│   └── README.md        # Backend documentation
│
└── frontend/            ✅ Complete
    ├── app/             # Next.js App Router
    ├── components/      # React components
    ├── lib/             # Utils and API client
    └── README.md        # Frontend documentation
```

## 🏃 Quick Start

### 1. Start Backend

```bash
# Start PostgreSQL with Docker
docker-compose up -d

# Start FastAPI server
cd backend
uvicorn main:app --reload

# Backend running at http://localhost:8000
```

### 2. Start Frontend

```bash
# Go to frontend folder
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev

# Frontend running at http://localhost:3000
```

### 3. Open your browser
- **Frontend:** http://localhost:3000
- **API Docs:** http://localhost:8000/docs

**Note:** Database initializes automatically, no need to run additional scripts.

## 🔗 Quick Access

**Frontend (Main Interface):**
- **Home:** http://localhost:3000 ← Start here 🏠
- **Register:** http://localhost:3000/register
- **Login:** http://localhost:3000/login
- **Dashboard:** http://localhost:3000/dashboard (requires login)

**Backend (API):**
- **API Documentation:** http://localhost:8000/docs
- **System Health:** http://localhost:8000/health
- **WebSocket Test Client:** http://localhost:8000/ws/test-client

## 📖 Documentation

### Complete Guides
- [QUICKSTART_FULLSTACK.md](QUICKSTART_FULLSTACK.md) - Complete Full-Stack guide 🆕
- [LANGUAGE_GUIDELINES.md](LANGUAGE_GUIDELINES.md) - Language standards for the project 🆕
- [STATUS.md](STATUS.md) - Development status and progress

### Backend Documentation
- [backend/README.md](backend/README.md) - Backend overview
- [backend/SETUP.md](backend/SETUP.md) - Detailed setup guide
- [backend/AUTHENTICATION.md](backend/AUTHENTICATION.md) - Authentication system 🆕
- [backend/WEBSOCKET.md](backend/WEBSOCKET.md) - Real-time chat 🆕
- [backend/STRUCTURE.md](backend/STRUCTURE.md) - Code architecture
- [backend/PHASE1_COMPLETED.md](backend/PHASE1_COMPLETED.md) - Medical data models
- [backend/PHASE2_COMPLETED.md](backend/PHASE2_COMPLETED.md) - User context integration

### Frontend Documentation
- [froStep-by-Step Development

This project is built in educational phases:

### Phase 1: Basic Backend ✅ 
- Simple REST API
- Basic endpoints
- No database

### Phase 2: Database ✅
- PostgreSQL with Docker
- Data models
- CRUD operations
- Automatic initialization
- Statistics system

### Phase 3: AI Integration ✅
- LangChain integrated
- OpenAI GPT and Anthropic Claude support
- Intelligent chat with medical context
- Intelligent fallback system

### Phase 4: Authentication ✅
- User registration with validation
- Login with JWT
- Protected routes
- Password hashing with bcrypt
- Token management (7-day expiration)

### Phase 5: Real-time Chat ✅
- WebSocket with JWT authentication
- Multiple users support
- Typing indicators
- Complete AI integration
- Interactive HTML test client

### Phase 6: Medical Data Models ✅
- MedicalProfile model
- Conversation and Message models
- MedicalDocument model
- Complete CRUD endpoints
- Database migration

### Phase 7: User Context Integration ✅
- MedicalContextService
- Personalized AI responses
- Conversation history
- Automatic message persistence
- Context-aware chat

### Phase 8: Frontend ✅
- Next.js 14 with TypeScript
- Login and registration pages
- Chat interface with WebSocket
- User dashboard
- Modern UI with Tailwind CSS
- State management with Zustand

### Phase 9: Advanced Features (Next)
- RAG with vector store
- LangGraph for intelligent flows
- Medical profile UI
- Document processing
- Conversation management

## 🤝 Best Practices

- ✅ All code in English
- ✅ Type hints in Python
- ✅ Complete docstrings
- ✅ Clean and commented code
- ✅ No hardcoded secrets
- ✅ Organized structure

## 📝 Notes

- Educational step-by-step project
- Each phase must work before continuing
- Learn each part thoroughly
- Consult documentation when in doubt

## 🆘 Help

If something doesn't work:
1. Verify the virtual environment is activated
2. Check that you installed dependencies
3. Read the backend README.md
4. Review the server logs

---

**Let's build something amazingependencias
3. Lee el README.md del backend
4. Revisa los logs del servidor

---

**¡Construyamos algo increíble! 🚀**
