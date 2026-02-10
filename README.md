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
| Frontend | Next.js | ⏳ Por crear |
| Backend | FastAPI | ✅ Fase 2 completa |
| Base de Datos | PostgreSQL | ✅ Funcionando (puerto 5433) |
| IA | LangGraph + LLM | ⏳ Fase posterior |
| Cache | Redis | ⏳ Fase posterior |
| WebSocket | FastAPI WS | ⏳ Fase posterior |
| Contenedores | Docker | ✅ PostgreSQL en Docker |

## 🚀 Estado Actual: Fase 2 - Backend Mejorado

### ✅ Completado
- API REST funcionando con FastAPI
- **Inicialización automática de base de datos** 🆕
- Endpoints CRUD completos (users, appointments)
- PostgreSQL con Docker (puerto 5433)
- **Sistema de estadísticas** 🆕
- Documentación automática
- Estructura del proyecto lista
- **Sin warnings de Pydantic** 🆕

### ⏳ Próximos Pasos
1. ~~Conectar PostgreSQL con Docker~~ ✅
2. ~~Crear modelos de base de datos~~ ✅
3. Sistema de autenticación (registro/login con JWT)
4. Integrar IA con LangGraph
5. Frontend con Next.js
6. WebSocket para chat en tiempo real

## 📁 Estructura del Proyecto

```
medical-ai-assistant/
├── backend/              ✅ Fase 1 completa
│   ├── main.py          # API FastAPI
│   ├── requirements.txt # Dependencias
│   └── README.md        # Documentación backend
│
└── frontend/            ⏳ Por crear en Fase 4
    └── (Next.js aquí)
```

## 🏃 Inicio Rápido

### Backend (¡Listo para usar!)

```bash
# 1. Iniciar PostgreSQL con Docker
docker-compose up -d

# 2. Ir a la carpeta backend e iniciar servidor
cd backend
python -m uvicorn main:app --reload

# 3. ¡Listo! Abre tu navegador
# http://localhost:8000/docs
```

**¡Nuevo!** La base de datos se inicializa automáticamente, no necesitas ejecutar scripts adicionales.

### Probar la API
- **Documentación interactiva:** http://localhost:8000/docs
- **Estado del sistema:** http://localhost:8000/health
- **Estadísticas:** http://localhost:8000/stats 🆕
- **Info del proyecto:** http://localhost:8000/info

📖 **Guía detallada:** Ver [QUICKSTART.md](QUICKSTART.md) para más ejemplos

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
- Inicialización automática 🆕
- Sistema de estadísticas 🆕

### Fase 3: Autenticación (Próximo)
- Registro de usuarios
- Login con JWT
- Protección de endpoints

### Fase 4: Inteligencia Artificial
- Registro de usuarios
- Login con JWT
- Rutas protegidas

### Fase 4: Frontend
- Next.js setup
- Páginas de login/registro
- Interfaz de chat

### Fase 5: Chat en Tiempo Real
- WebSocket
- Mensajes en vivo

### Fase 6: Inteligencia Artificial
- LangGraph para decisiones
- LLM para respuestas
- Detección de intenciones

### Fase 7: Features Avanzadas
- Sistema de citas
- Gestión de documentos
- Notificaciones

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
