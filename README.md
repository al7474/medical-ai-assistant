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
| Frontend | Next.js 14 + TypeScript | ✅ Basic Complete |
| Backend | FastAPI | ✅ Complete |
| Database | PostgreSQL | ✅ Running (port 5433) |
| AI | LangChain + OpenAI/Anthropic | ✅ Configured |
| Vector Store | FAISS | ✅ RAG implemented |
| Embeddings | OpenAI text-embedding-ada-002 | ✅ Phase 3 complete |
| Authentication | JWT | ✅ Complete |
| WebSocket | FastAPI WS | ✅ Real-time chat |
| Document Processing | PyPDF2 | ✅ PDF extraction |
| Styling | Tailwind CSS | ✅ Complete |
| State Management | Zustand | ✅ Complete |
| Cache | Redis | ⏳ Phase 6 |
| Containers | Docker | ✅ PostgreSQL |

## 🚀 Current Status: Phase 3 - RAG Complete ✅

### ✅ Phase 1: Medical Data Models (Complete)
- Complete medical profile system (age, BMI, blood type)
- Medical conditions tracking (diagnoses, severity)
- Medications management (prescriptions, dosage)
- Allergies system (allergen, reactions)
- Medical documents model
- Full CRUD operations
📖 **[PHASE1_COMPLETED.md](PHASE1_COMPLETED.md)**

### ✅ Phase 2: User Context Integration (Complete)
- Conversation history storage
- Medical context retrieval service
- WebSocket chat with context
- Personalized AI responses
- Recent conversation memory
📖 **[PHASE2_COMPLETED.md](PHASE2_COMPLETED.md)**

### ✅ Phase 3: RAG Implementation (Complete) 🆕
- **Vector store with FAISS** (semantic search)
- **Document processing service** (PDF extraction)
- **OpenAI embeddings** integration
- **6 document management endpoints**
- **Document-aware AI responses**
- **Per-user vector stores**
- **Graceful degradation** (works without API key)
📖 **[PHASE3_COMPLETED.md](PHASE3_COMPLETED.md)** 🆕

### ✅ Frontend Basic Implementation (Complete)
- Next.js 14 with TypeScript
- Authentication (login/register)
- Real-time chat interface with WebSocket
- Dashboard with medical assistant
- Tailwind CSS styling
- State management with Zustand
- Protected routes and JWT handling

### 🚧 Next Phases
- **Phase 4:** LangGraph workflows (agent orchestration, multi-step reasoning) ⏳ **NEXT**
- **Phase 5:** Advanced Frontend UI (medical dashboard, visualizations, document viewer)
- **Phase 6:** Optimizations (caching, testing, production deployment)

## 📁 Project Structure

```
medical-ai-assistant/
├── backend/                      ✅ Complete
│   ├── main.py                   # FastAPI application
│   ├── models/                   # Database models
│   │   ├── medical_profile.py    # Medical data
│   │   ├── medical_document.py   # Document storage
│   │   └── conversation.py       # Chat history
│   ├── services/                 # Business logic
│   │   ├── chat_service.py       # AI chat with LangChain
│   │   ├── vector_store_service.py # FAISS vector store (RAG)
│   │   ├── document_processing_service.py # PDF processing
│   │   └── user_context_service.py # Context retrieval
│   ├── api/routes/               # API endpoints
│   │   ├── chat.py               # REST chat
│   │   ├── websocket.py          # WebSocket chat
│   │   ├── medical_documents.py  # Document upload 🆕
│   │   └── medical_profile.py    # Medical data
│   └── data/vectorstore/         # Vector stores per user
│
└── frontend/                     ✅ Running
    ├── app/                      # Next.js App Router
    ├── components/               # React components
    ├── lib/                      # Utils and API client
    └── README.md                 # Frontend documentation
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

This project is built in structured phases:

### Phase 1: Medical Data Models ✅ 
- Complete medical profile (age, weight, blood type, BMI)
- Medical conditions tracking with severity
- Medications management with dosage
- Allergies system with reaction severity
- Medical documents model
- Full CRUD operations for all medical data
📖 [PHASE1_COMPLETED.md](PHASE1_COMPLETED.md)

### Phase 2: User Context Integration ✅
- Conversation history storage
- User context retrieval service
- Medical profile summarization
- Recent conversation memory (last 10 messages)
- Context-aware AI prompts
- WebSocket and REST integration
📖 [PHASE2_COMPLETED.md](PHASE2_COMPLETED.md)

### Phase 3: RAG (Retrieval Augmented Generation) ✅
- FAISS vector store for semantic search
- PDF document processing with PyPDF2
- OpenAI embeddings (text-embedding-ada-002)
- Document upload endpoints (PDF and text)
- Semantic document search
- Document-aware AI responses
- Per-user vector store isolation
📖 [PHASE3_COMPLETED.md](PHASE3_COMPLETED.md) 🆕

### Phase 4: LangGraph Workflows ⏳ (Next)
- Agent orchestration
- Multi-step reasoning
- Tool calling (appointments, documents, medical data)
- State persistence
- Autonomous task execution

### Phase 5: Frontend Medical UI ⏳
- Medical dashboard with visualizations
- Document viewer and manager
- Real-time chat interface
- Medical profile management
- Analytics and insights

### Phase 6: Optimizations & Production ⏳
- Redis caching
- Response streaming
- Background job processing
- Unit and integration tests
- Production deployment
- CI/CD pipeline

## 🤝 Best Practices

- ✅ All code in English (technical documentation)
- ✅ Spanish for end-user interfaces
- ✅ Type hints in Python and TypeScript
- ✅ Complete docstrings
- ✅ Clean and commented code
- ✅ No hardcoded secrets
- ✅ Organized structure
- ✅ Comprehensive error handling

## 📖 Documentation

- **[STATUS.md](STATUS.md)** - Current project status and progress
- **[PHASE1_COMPLETED.md](PHASE1_COMPLETED.md)** - Medical data models
- **[PHASE2_COMPLETED.md](PHASE2_COMPLETED.md)** - User context integration
- **[PHASE3_COMPLETED.md](PHASE3_COMPLETED.md)** - RAG implementation 🆕
- **[LANGUAGE_GUIDELINES.md](LANGUAGE_GUIDELINES.md)** - Language standards
- **[PROJECT_GUIDELINES.md](PROJECT_GUIDELINES.md)** - Development guidelines

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
