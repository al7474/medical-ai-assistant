# 🌐 Language Guidelines

## Overview

This document establishes the language standards for the Medical AI Assistant project to ensure consistency and clarity across all project artifacts.

## 📋 Language Rules

### ✅ Use English For:

1. **All Technical Documentation**
   - README files for development setup
   - API documentation
   - Architecture documents
   - Setup and configuration guides
   - Phase completion reports
   - Code structure documentation

2. **All Code**
   - Variable names
   - Function names
   - Class names
   - Comments and docstrings
   - Commit messages
   - Pull request descriptions

3. **Developer-Facing Content**
   - Error messages in logs
   - Debug output
   - Database migration scripts
   - Configuration files
   - Environment variable names

### 🇪🇸 Use Spanish For:

1. **End-User Facing Content**
   - Frontend UI text and labels
   - User-facing error messages
   - Email templates sent to users
   - Push notifications
   - Help text in the application
   - User guides and tutorials

2. **Main Project Description**
   - Main README.md overview section (project vision, features for end-users)
   - Marketing materials
   - User-facing documentation

## 📁 File-by-File Guidelines

### English Only:
- `README.md` (root) - Main project documentation
- `STATUS.md` - Development status
- `QUICKSTART.md` - Developer quick start
- `QUICKSTART_FULLSTACK.md` - Full stack setup
- `AI_SETUP.md` - AI configuration
- `backend/SETUP.md` - Backend setup
- `backend/STRUCTURE.md` - Code structure
- `backend/AUTHENTICATION.md` - Auth system docs
- `backend/WEBSOCKET.md` - WebSocket docs
- `backend/PHASE*.md` - Phase completion reports
- `frontend/README.md` - Frontend setup
- All files in `backend/api/`, `backend/models/`, `backend/services/`
- All `.py` files
- All `.ts` and `.tsx` files

### Spanish for User Content:
- `frontend/app/` components - UI text, labels, messages
- `frontend/components/` - User-facing strings
- Email templates (when created)
- User documentation (when created)

## 🔍 Examples

### ✅ Good - Technical Documentation (English):

```markdown
# Phase 1: Medical Data Models

## Implementation Complete

### Created Models

1. **MedicalProfile** - Complete user medical profile
2. **Conversation** - Chat session management
3. **Message** - Individual chat messages
```

### ❌ Bad - Technical Documentation (Spanish):

```markdown
# Fase 1: Modelos de Datos Médicos

## Implementación Completada

### Modelos Creados

1. **MedicalProfile** - Perfil médico completo del usuario
```

### ✅ Good - User Interface (Spanish):

```typescript
// frontend/app/login/page.tsx
<button>Iniciar Sesión</button>
<p>¿No tienes cuenta? Regístrate aquí</p>
```

### ✅ Good - Code Comments (English):

```python
# backend/services/chat_service.py
def get_full_context(self, user_id: int, include_history: bool = True):
    """
    Retrieves comprehensive medical context for the user.
    
    Args:
        user_id: The ID of the user
        include_history: Whether to include conversation history
        
    Returns:
        Dictionary containing medical profile and chat history
    """
```

## 🛠️ Enforcement

### Pre-Commit Checklist:
- [ ] All technical docs are in English
- [ ] All code comments are in English
- [ ] All commit messages are in English
- [ ] User-facing strings are in Spanish
- [ ] Variable/function names are in English

### Code Review Checklist:
- [ ] No Spanish in technical documentation
- [ ] No English in user-facing UI text
- [ ] Consistent language use throughout files

## 🔄 Migration Strategy

When converting existing Spanish documentation to English:

1. **Identify the document type** - Is it technical or user-facing?
2. **Translate if technical** - Convert all Spanish content to English
3. **Keep structure** - Maintain the same headings, formatting, and organization
4. **Update references** - Ensure all links and cross-references still work
5. **Verify accuracy** - Technical terms should be properly translated

## 📝 Quick Reference

| Content Type | Language | Example |
|--------------|----------|---------|
| API Documentation | 🇬🇧 English | "Create a new user endpoint" |
| Database Models | 🇬🇧 English | `class MedicalProfile(Base)` |
| Frontend Labels | 🇪🇸 Spanish | "Iniciar Sesión" |
| Error Logs | 🇬🇧 English | "Database connection failed" |
| User Messages | 🇪🇸 Spanish | "Registro exitoso" |
| Commit Messages | 🇬🇧 English | "feat: add medical profile endpoint" |
| Code Comments | 🇬🇧 English | "# Calculate BMI from height and weight" |
| Button Text | 🇪🇸 Spanish | "Enviar mensaje" |

## 🎯 Rationale

### Why English for Technical Content?
- **International Collaboration** - Enables developers worldwide to contribute
- **Industry Standard** - Most programming resources are in English
- **Better Tooling** - Code analysis tools work better with English
- **Knowledge Sharing** - Easier to share solutions with the global community

### Why Spanish for User Content?
- **Target Audience** - Primary users speak Spanish
- **Better UX** - Users understand and trust content in their native language
- **Accessibility** - Medical information should be in the user's preferred language
- **Legal Compliance** - May be required for medical applications in Spanish-speaking regions

## 🤝 Contributing

When contributing to this project:

1. Read these guidelines carefully
2. Follow the language rules for each type of content
3. Ask if you're unsure about a specific case
4. Review your changes before submitting

## 📚 Related Documents

- [PROJECT_GUIDELINES.md](PROJECT_GUIDELINES.md) - General project guidelines
- [backend/README.md](backend/README.md) - Backend documentation
- [frontend/README.md](frontend/README.md) - Frontend documentation

---

**Remember:** Technical documentation = English 🇬🇧 | User interface = Spanish 🇪🇸
