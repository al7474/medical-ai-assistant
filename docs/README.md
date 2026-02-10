# 📚 Medical AI Assistant - Documentation

Complete documentation for the Medical AI Assistant project.

## 📖 Table of Contents

### 🚀 Getting Started
- [Quick Start Guide](../QUICKSTART.md) - Fast setup and run
- [Project Guidelines](../PROJECT_GUIDELINES.md) - Development guidelines
- [Project Status](../STATUS.md) - Current progress and roadmap

### ⚙️ Setup & Configuration
- [AI Providers Setup](setup/ai-providers.md) - Configure OpenAI, Anthropic, Gemini
- [Full Stack Quick Start](setup/quickstart-fullstack.md) - Complete setup guide
- [Language Guidelines](setup/language-guidelines.md) - Bilingual requirements

### 🏗️ Architecture
- [Backend Structure](architecture/backend-structure.md) - Backend architecture overview
- [Refactoring Notes](architecture/refactoring-notes.md) - Code refactoring history
- [API Documentation](api/) - API endpoints and usage

### 🔌 API Documentation
- [Authentication](api/authentication.md) - JWT authentication system
- [WebSocket Protocol](api/websocket.md) - Real-time chat WebSocket API

### 📅 Development Phases
- [Phase 1 - Core Backend](phases/phase-1.md) - Database, models, basic API
- [Phase 2 - AI Integration](phases/phase-2.md) - OpenAI chat integration
- [Phase 3 - Document Processing](phases/phase-3.md) - PDF/image processing, RAG
- [Phase 4 - LangGraph Agent](phases/phase-4.md) - Multi-tool autonomous agent

### 🧪 Testing
- [Testing Guide](../backend/docs/testing/TESTING_GUIDE.md) - Complete testing documentation
- [Test Organization](../backend/docs/testing/test-organization.md) - Test structure
- [Tests Ready](../backend/docs/testing/tests-ready.md) - Quick test start
- [Tests README](../backend/tests/README.md) - Running tests

---

## 📂 Documentation Structure

```
docs/
├── README.md (this file)          # Documentation index
│
├── setup/                          # Setup and configuration
│   ├── ai-providers.md            # AI services setup
│   ├── quickstart-fullstack.md    # Complete setup
│   └── language-guidelines.md     # Bilingual guidelines
│
├── phases/                         # Development history
│   ├── phase-1.md                 # Core backend
│   ├── phase-2.md                 # AI integration
│   ├── phase-3.md                 # Document processing
│   └── phase-4.md                 # LangGraph agent
│
├── api/                            # API documentation
│   ├── authentication.md          # Auth system
│   └── websocket.md               # WebSocket protocol
│
└── architecture/                   # System architecture
    ├── backend-structure.md       # Backend overview
    └── refactoring-notes.md       # Refactoring history
```

---

## 🔍 Quick Links

### For Developers
- **First Time Setup**: [Quick Start Guide](../QUICKSTART.md)
- **Backend Setup**: [Backend README](../backend/README.md) → [Backend Setup](../backend/SETUP.md)
- **Frontend Setup**: [Frontend README](../frontend/README.md)
- **Running Tests**: [Testing Guide](../backend/docs/testing/TESTING_GUIDE.md)

### For Understanding the System
- **Architecture**: [Backend Structure](architecture/backend-structure.md)
- **Authentication**: [Authentication Guide](api/authentication.md)
- **WebSocket Chat**: [WebSocket Protocol](api/websocket.md)
- **AI Configuration**: [AI Providers](setup/ai-providers.md)

### Phase-by-Phase Progress
1. [Phase 1](phases/phase-1.md) - Database & Basic API ✅
2. [Phase 2](phases/phase-2.md) - AI Chat Integration ✅
3. [Phase 3](phases/phase-3.md) - Document Processing ✅
4. [Phase 4](phases/phase-4.md) - LangGraph Agent ✅
5. Phase 5 - Frontend (In Progress)

---

## 📝 Contributing

When adding new documentation:
1. Place in appropriate subdirectory
2. Update this index
3. Use clear, descriptive filenames
4. Include code examples where helpful
5. Keep language consistent (English/Spanish as needed)

---

## 🆘 Need Help?

- **Setup Issues**: Check [Quick Start](../QUICKSTART.md) or [AI Setup](setup/ai-providers.md)
- **API Questions**: See [API Documentation](api/)
- **Testing Problems**: Read [Testing Guide](../backend/docs/testing/TESTING_GUIDE.md)
- **Architecture Questions**: Review [Backend Structure](architecture/backend-structure.md)

---

**Last Updated**: February 2026  
**Project Status**: Phase 4 Complete, Phase 5 In Progress
