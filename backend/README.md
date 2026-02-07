# Medical AI Assistant - Backend

REST API for an intelligent medical assistant.

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

- `GET /` - Welcome
- `GET /health` - System health
- `GET /hello/{name}` - Personalized greeting
- `POST /chat` - Send message to bot
- `GET /info` - Project information
- `GET /test-responses` - See available responses

## 🛠️ Next Steps

1. ✅ Basic backend working
2. ⏳ Add database (PostgreSQL)
3. ⏳ Authentication system (JWT)
4. ⏳ Integrate AI (LangGraph + LLM)
5. ⏳ WebSocket for real-time chat
6. ⏳ Frontend with Next.js

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
