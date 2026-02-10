# 🚀 Quick Start Guide - Medical AI Assistant

## ⚡ Start Everything (3 Commands)

```powershell
# 1. Start PostgreSQL (if not running)
docker-compose up -d

# 2. Run the API (from backend folder)
cd backend
python -m uvicorn main:app --reload

# 3. Open in browser
# http://localhost:8000/docs
```

That's it! The API now **auto-initializes** the database tables on startup.

---

## 🧪 Test the API

### Using Swagger UI (Recommended)
1. Go to http://localhost:8000/docs
2. Click on any endpoint
3. Click "Try it out"
4. Fill in the data
5. Click "Execute"

### Using curl

**Create a user:**
```bash
curl -X POST "http://localhost:8000/users/" -H "Content-Type: application/json" -d '{"name": "John Doe", "email": "john@example.com"}'
```

**Get all users:**
```bash
curl http://localhost:8000/users/
```

**Create an appointment:**
```bash
curl -X POST "http://localhost:8000/appointments/" -H "Content-Type: application/json" -d '{"user_id": 1, "description": "Annual checkup"}'
```

**Get all appointments:**
```bash
curl http://localhost:8000/appointments/
```

**Get statistics:**
```bash
curl http://localhost:8000/stats
```

---

## 📊 Available Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Welcome message |
| GET | `/health` | Health check |
| GET | `/info` | Project information |
| GET | `/stats` | 📊 System statistics |
| POST | `/users/` | Create new user |
| GET | `/users/` | List all users |
| POST | `/appointments/` | Create appointment |
| GET | `/appointments/` | List appointments |
| GET | `/appointments/{id}` | Get specific appointment |
| DELETE | `/appointments/{id}` | Delete appointment |
| POST | `/chat` | Chat with bot (simple) |

---

## 🔧 Useful Commands

```powershell
# Check if PostgreSQL is running
docker ps

# View PostgreSQL logs
docker logs medical-ai-db

# Stop PostgreSQL
docker-compose down

# Restart PostgreSQL with fresh data
docker-compose down -v
docker-compose up -d

# Access PostgreSQL directly
docker exec -it medical-ai-db psql -U medical_user -d medical_db
```

---

## 🎯 What's New (Step 2 Improvements)

✅ **Auto-initialization** - No need to run `init_db.py` manually  
✅ **Fixed Pydantic warnings** - Updated to Pydantic V2 syntax  
✅ **Statistics endpoint** - Track users and appointments  
✅ **Better error messages** - Clear feedback on startup  

---

## 🐛 Troubleshooting

**Port 5432 already in use?**
- ✅ Already fixed! Using port 5433 for Docker

**Database connection error?**
- Make sure Docker is running: `docker ps`
- Restart container: `docker-compose restart`

**uvicorn not found?**
- Use: `python -m uvicorn main:app --reload`

---

## 📝 Next Steps

Now that the backend is solid, you can:
1. ✅ Add authentication (JWT, login, register)
2. ✅ Create frontend with Next.js
3. ✅ Integrate AI with LangGraph + LLM
4. ✅ Add WebSocket for real-time chat

Ready to continue? 🚀
