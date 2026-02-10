# 🚀 Guía de Inicio Rápido - Full Stack

## ✅ Lo que tienes funcionando

1. **Backend** (puerto 8000) ✅
   - API REST con FastAPI
   - PostgreSQL database
   - Autenticación JWT
   - WebSocket real-time chat
   - AI integration

2. **Frontend** (puerto 3000) ✅  
   - Next.js 14 con TypeScript
   - Interfaz moderna con Tailwind CSS
   - Login y registro
   - Chat en tiempo real
   - WebSocket conectado

## 🎯 Cómo Probar Todo

### Opción 1: Usar la Interfaz Web (Recomendado)

1. **Abre el navegador:**
   ```
   http://localhost:3000
   ```

2. **Regístrate:**
   - Click en "Registrarse"
   - Completa el formulario
   - Se creará tu cuenta automáticamente

3. **Inicia sesión:**
   - Te redirigirá automáticamente al dashboard
   - O ve a "Iniciar Sesión" si ya tienes cuenta

4. **Chatea con la IA:**
   - En el dashboard verás el chat
   - Escribe un mensaje como: "Hola, ¿qué haces?"
   - La IA te responderá en tiempo real vía WebSocket
   - Verás indicadores de "escribiendo..." mientras procesa

### Opción 2: Probar el Backend Directamente

1. **API Docs (Swagger):**
   ```
   http://localhost:8000/docs
   ```

2. **Test Client WebSocket:**
   ```
   http://localhost:8000/ws/test-client
   ```

## 📋 Verificar que Todo Funciona

### Backend Checklist

```bash
# 1. Backend corriendo
curl http://localhost:8000/health

# 2. Base de datos conectada
curl http://localhost:8000/stats

# 3. WebSocket disponible
# Usa el test client: http://localhost:8000/ws/test-client
```

### Frontend Checklist

- ✅ Home page carga en http://localhost:3000
- ✅ Puedes navegar a /login y /register
- ✅ Puedes crear una cuenta
- ✅ Puedes iniciar sesión
- ✅ El dashboard muestra el chat
- ✅ WebSocket se conecta (indicador verde)
- ✅ Puedes enviar mensajes
- ✅ Recibes respuestas de la IA

## 🔧 Comandos Útiles

### Backend
```bash
# Iniciar backend
cd backend
uvicorn main:app --reload

# Ejecutar tests
python test_auth.py
python test_websocket.py
```

### Frontend
```bash
# Iniciar frontend
cd frontend
npm run dev

# Build para producción
npm run build
npm start
```

## 🎨 Funcionalidades Implementadas

### Autenticación
- ✅ Registro de usuarios con validación
- ✅ Login con JWT (tokens de 7 días)
- ✅ Logout
- ✅ Rutas protegidas
- ✅ Persistencia de sesión (localStorage)

### Chat en Tiempo Real
- ✅ WebSocket bidireccional
- ✅ Autenticación por token
- ✅ Múltiples usuarios simultáneos
- ✅ Indicadores de estado de conexión
- ✅ Indicadores de "escribiendo..."
- ✅ Integración con AI (OpenAI/Anthropic o fallback)

### UI/UX
- ✅ Diseño moderno y responsive
- ✅ Animaciones suaves
- ✅ Feedback visual en todo momento
- ✅ Manejo de errores amigable
- ✅ Auto-scroll en chat

## 🐛 Solución de Problemas

### Frontend no carga

```bash
# Ir a la carpeta correcta
cd C:\Users\al\Downloads\P\personal\GitDesk\medical-ai-assistant\frontend

# Reinstalar dependencias
npm install

# Iniciar servidor
npm run dev
```

### Backend no conecta

```bash
# Verificar que backend esté corriendo
# En otra terminal:
cd backend
uvicorn main:app --reload
```

### WebSocket no conecta

1. Verifica que estés autenticado (inicia sesión)
2. Verifica que el backend esté corriendo
3. Revisa la consola del navegador (F12)
4. El indicador debe estar verde cuando conectado

### Error de CORS

El backend ya tiene CORS configurado para `localhost:3000`.  
Si cambias el puerto del frontend, actualiza `backend/main.py`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # ← Cambia aquí
    ...
)
```

## 🌟 Próximos Pasos

1. **Probar todo el sistema** ✅ (¡estás aquí!)
2. **Configurar API key de OpenAI** (opcional, para IA real)
3. **Añadir más features:**
   - Historial de conversaciones
   - Múltiples salas de chat
   - Upload de archivos
   - Notificaciones
4. **Deploy a producción:**
   - Frontend → Vercel
   - Backend → Railway/Heroku/AWS
   - Database → PostgreSQL managed

## 📊 Estado del Proyecto

**Progreso: ~85%** 🎉

- [x] Backend API REST
- [x] PostgreSQL database
- [x] AI integration (LangChain)
- [x] Autenticación JWT
- [x] WebSocket real-time
- [x] Frontend Next.js
- [x] UI moderna
- [x] Integración completa
- [ ] Deploy a producción
- [ ] Features avanzadas

## 🎉 ¡Felicitaciones!

Tienes un **asistente médico con IA completamente funcional** con:
- ✨ Full-stack (Frontend + Backend)
- 🔐 Autenticación segura
- 💬 Chat en tiempo real
- 🤖 Integración con IA
- 🎨 UI moderna y profesional

---

**¿Preguntas?** Revisa:
- [README.md](README.md) - Overview general
- [backend/README.md](backend/README.md) - Documentación backend
- [backend/AUTHENTICATION.md](backend/AUTHENTICATION.md) - Sistema de auth
- [backend/WEBSOCKET.md](backend/WEBSOCKET.md) - Chat en tiempo real
- [frontend/README.md](frontend/README.md) - Documentación frontend
