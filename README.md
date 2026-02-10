# 🏥 Medical AI Assistant

Asistente médico inteligente que conversa con pacientes, entiende sus necesidades y gestiona citas y documentos automáticamente.

## 🎯 Visión del Proyecto

Un asistente médico con IA que:
- 💬 Conversa naturalmente con pacientes
- 🤖 Entiende intenciones y contexto
- 📅 Gestiona citas automáticamente
- 📄 Maneja documentos médicos
- 🔒 Seguro y confiable

## 🛠️ Tech Stack

| Componente | Tecnología | Estado |
|------------|------------|--------|
| Frontend | Next.js 14 + TypeScript | ✅ Fase 7 completa |
| Backend | FastAPI | ✅ Fase 6 completa |
| Base de Datos | PostgreSQL | ✅ Funcionando (puerto 5433) |
| IA | LangChain + LLM | ✅ Configurado (requiere API key) |
| Autenticación | JWT | ✅ Completa |
| WebSocket | FastAPI WS | ✅ Real-time chat funcionando |
| Cache | Redis | ⏳ Fase posterior |
| Contenedores | Docker | ✅ PostgreSQL en Docker |

## 🚀 Estado Actual: Fase 7 - Frontend Completo ✅

### ✅ Completado
- API REST funcionando con FastAPI
- **Inicialización automática de base de datos**
- Endpoints CRUD completos (users, appointments)
- PostgreSQL con Docker (puerto 5433)
- **Sistema de estadísticas**
- **AI Chat Service con LangChain** 🤖✨
- **Soporte para OpenAI GPT y Anthropic Claude**
- **Fallback inteligente sin API key**
- **Sistema de Autenticación JWT completo** 🔐
  - Registro de usuarios con validación
  - Login con tokens JWT
  - Rutas protegidas
  - Password hashing con bcrypt
- **WebSocket para chat en tiempo real** 🌐✨
  - Conexiones autenticadas con JWT
  - Soporte para múltiples usuarios simultáneos
  - Indicadores de escritura
  - Integración con IA
  - Test client HTML interactivo
- **Frontend Next.js 14 completo** 💎✨
  - Interfaz moderna con Tailwind CSS
  - Páginas de login y registro
  - Dashboard con chat en tiempo real
  - Integración completa con WebSocket
  - State management con Zustand
  - Completamente tipado con TypeScript
- Documentación automática
- Estructura del proyecto lista
- Sin warnings de Pydantic
~~Frontend con Next.js~~ ✅
7. **Features avanzadas** (historial de chat, notificaciones, roles)
8. **Deploy a producción** (Docker, CI/CD, monitoring
1. ~~Conectar PostgreSQL con Docker~~ ✅
2. ~~Crear modelos de base de datos~~ ✅
3. ~~Integrar AI con LangChain~~ ✅
4. ~~Sistema de autenticación (registro/login con JWT)~~ ✅
5. ~~WebSocket para chat en Completo
│   ├── main.py          # API FastAPI
│   ├── models.py        # Modelos DB
│   ├── database.py      # PostgreSQL
│   ├── services/        # Lógica de negocio
│   ├── api/routes/      # Endpoints
│   └── README.md        # Documentación
│
└── frontend/            ✅ Completo
    ├── app/             # Next.js App Router
    ├── components/      # React components
    ├── lib/             # Utils y API client
    └── README.md        # Documentación
medical-ai-assistant/
├── backend/              ✅ Fase 1 completa
│   ├── main.py          # API FastAPI
│   ├── requirements.txt # Dependencias
│   └── README.md        # Documentación backend
│1. Iniciar Backend

```bash
# Iniciar PostgreSQL con Docker
docker-compose up -d

# Iniciar servidor FastAPI
cd backend
uvicorn main:app --reload

# Backend corriendo en http://localhost:8000
```

### 2. Iniciar Frontend

```bash
# EnAcceso Rápido

**Frontend (Interfaz Principal):**
- **Home:** http://localhost:3000 ← Comienza aquí 🏠
- **Registro:** http://localhost:3000/register
- **Login:** http://localhost:3000/login
- **Dashboard:** http://localhost:3000/dashboard (requiere login)

**Backend (API):**
- **Documentación API:** http://localhost:8000/docs
- **Estado del sistema:** http://localhost:8000/health
- **Test Client WebSocket:** http://localhost:8000/ws/test-client

📖 **Guías completas:**
- [QUICKSTART_FULLSTACK.md](QUICKSTART_FULLSTACK.md) - Guía completa Full-Stack 🆕
- [backend/README.md](backend/README.md) - Documentación backend
- [backend/AUTHENTICATION.md](backend/AUTHENTICATION.md) - Sistema de autenticación
- [backend/WEBSOCKET.md](backend/WEBSOCKET.md) - Chat en tiempo real
- [frontend/README.md](frontend/README.md) - Documentación frontend
# 3. ¡Listo! Abre tu navegador
# http://localhost:8000/docs
```

**¡Nuevo!** La base de datos se inicializa automáticamente, no necesitas ejecutar scripts adicionales.

### Probar la API
- **Documentación interactiva:** http://localhost:8000/docs
- **Estado del sistema:** http://localhost:8000/health
- **Estadísticas:** http://localhost:8000/stats
- **Info del proyecto:** http://localhost:8000/info
- **Chat con IA:** http://localhost:8000/docs (POST /chat) 🤖
- **Autenticación:**
  - Registro: POST /auth/register 🔐
  - Login: POST /auth/login 🔐
  - Ver perfil: GET /auth/me 🔐
- **WebSocket Chat en tiempo real:** ws://localhost:8000/ws/chat 🌐
- **Test Client WebSocket:** http://localhost:8000/ws/test-client ✨

📖 **Guías detalladas:**
- [QUICKSTART.md](QUICKSTART.md) - Inicio rápido
- [AI_SETUP.md](AI_SETUP.md) - Cómo configurar la IA
- [backend/AUTHENTICATION.md](backend/AUTHENTICATION.md) - Sistema de autenticación 🆕
- [backend/WEBSOCKET.md](backend/WEBSOCKET.md) - Chat en tiempo real 🆕

## 📖 Documentación

- [Backend README](backend/README.md) - Guía del backend

## 🎓 Aprendizaje Paso a Paso

Este proyecto se construye en fases educativas:

### Fase 1: Backend Básico ✅ 
- API REST simple
- Endpoints básicos
- Sin base de datos

### Fase 2: Base de Datos ✅
- PostgreSQL con Docker
- Modelos de datos
- CRUD operations
- Inicialización automática
- Sistema de estadísticas

### Fase 3: Integración de IA ✅
- LangChain integrado
- Soporte OpenAI GPT y Anthropic Claude
- Chat inteligente co✅
- Next.js 14 con TypeScript
- Páginas de login y registro
- Interfaz de chat con WebSocket
- Dashboard de usuario
- UI moderna con Tailwind CSS
- State management con Zustand

### Fase 8: Features Avanzadas (Próximo)
- Mejores prácticas
- Código limpio y mantenible

### Fase 5: Autenticación ✅
- Registro de usuarios con validación
- Login con JWT
- Rutas protegidas
- Password hashing con bcrypt
- Gestión de tokens (7 días de expiración)

### Fase 6: Chat en Tiempo Real ✅
- WebSocket con autenticación JWT
- Soporte para múltiples usuarios
- Indicadores de escritura
- Integración completa con IA
- Test client HTML interactivo

### Fase 7: Frontend (Próximo)
- Next.js setup
- Páginas de login/registro
- Interfaz de chat con WebSocket
- Dashboard de usuario

### Fase 8: Features Avanzadas
- Historial de conversaciones
- Sistema de citas médicas
- Gestión de documentos
- Notificaciones en tiempo real
- Roles y permisos avanzados

## 🤝 Mejores Prácticas

- ✅ Todo el código en inglés
- ✅ Type hints en Python
- ✅ Docstrings completos
- ✅ Código limpio y comentado
- ✅ Sin hardcodear secrets
- ✅ Estructura organizada

## 📝 Notas

- Proyecto educativo paso a paso
- Cada fase debe funcionar antes de continuar
- No te adelantes, aprende bien cada parte
- Consulta la documentación cuando tengas dudas

## 🆘 Ayuda

Si algo no funciona:
1. Verifica que el entorno virtual esté activado
2. Revisa que instalaste las dependencias
3. Lee el README.md del backend
4. Revisa los logs del servidor

---

**¡Construyamos algo increíble! 🚀**
