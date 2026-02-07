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
| Backend | FastAPI | ✅ Fase 1 completa |
| Base de Datos | PostgreSQL | ⏳ Próxima fase |
| IA | LangGraph + LLM | ⏳ Fase posterior |
| Cache | Redis | ⏳ Fase posterior |
| WebSocket | FastAPI WS | ⏳ Fase posterior |
| Contenedores | Docker | ⏳ Cuando sea necesario |

## 🚀 Estado Actual: Fase 1 - Backend Básico

### ✅ Completado
- API REST funcionando con FastAPI
- Endpoints básicos operativos
- Documentación automática
- Estructura del proyecto

### ⏳ Próximos Pasos
1. Conectar PostgreSQL con Docker
2. Crear modelos de base de datos
3. Sistema de autenticación (registro/login)
4. Integrar IA con LangGraph
5. Frontend con Next.js

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

### Backend (Fase Actual)

```bash
# Ir a la carpeta backend
cd backend

# Crear entorno virtual
python -m venv venv

# Activar entorno virtual (Windows)
.\venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar servidor
uvicorn main:app --reload
```

### Probar la API
- **Documentación:** http://localhost:8000/docs
- **Estado:** http://localhost:8000/health
- **Info:** http://localhost:8000/info

## 📖 Documentación

- [Backend README](backend/README.md) - Guía del backend

## 🎓 Aprendizaje Paso a Paso

Este proyecto se construye en fases educativas:

### Fase 1: Backend Básico ✅ 
- API REST simple
- Endpoints básicos
- Sin base de datos

### Fase 2: Base de Datos (Próximo)
- PostgreSQL con Docker
- Modelos de datos
- CRUD operations

### Fase 3: Autenticación
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
