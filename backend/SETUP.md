# 🚀 Setup Guide - Medical AI Assistant Backend

## Prerequisites
- Python 3.10 or higher
- Docker Desktop installed and running
- Git

## Step-by-Step Setup

### 1️⃣ Start PostgreSQL with Docker

```bash
# From the project root directory
docker-compose up -d
```

This will:
- Download PostgreSQL image (first time only)
- Create container named `medical-ai-db`
- Create database `medical_db`
- Create user `medical_user` with password `medical_pass`
- Expose PostgreSQL on port 5432

Verify it's running:
```bash
docker ps
# You should see: medical-ai-db container running
```

### 2️⃣ Setup Python Environment

```bash
# Navigate to backend folder
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows PowerShell:
.\venv\Scripts\Activate.ps1

# Windows CMD:
.\venv\Scripts\activate.bat

# Linux/Mac:
source venv/bin/activate
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- FastAPI & Uvicorn (API framework)
- SQLAlchemy & asyncpg (Database ORM)
- Pydantic (Data validation)
- python-dotenv (Environment variables)

### 4️⃣ Configure Environment (Optional)

```bash
# Copy example environment file
cp .env.example .env

# Edit .env if you need custom settings
# Default values should work fine
```

### 5️⃣ Initialize Database Tables

```bash
python init_db.py
```

Expected output:
```
🔄 Connecting to database...
🔄 Creating tables...
✅ Database tables created successfully!
📋 Tables created: users, appointments
```

### 6️⃣ Start the API Server

```bash
uvicorn main:app --reload
```

Expected output:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete.
```

### 7️⃣ Test the API

Open your browser and go to:
- **API Docs (Swagger UI):** http://localhost:8000/docs
- **Health Check:** http://localhost:8000/health
- **System Info:** http://localhost:8000/info

## 🧪 Testing Endpoints

### Create a User (POST)
```bash
curl -X POST "http://localhost:8000/users/" \
  -H "Content-Type: application/json" \
  -d '{"name": "John Doe", "email": "john@example.com"}'
```

### List All Users (GET)
```bash
curl http://localhost:8000/users/
```

### Create an Appointment (POST)
```bash
curl -X POST "http://localhost:8000/appointments/" \
  -H "Content-Type: application/json" \
  -d '{"user_id": 1, "description": "General checkup"}'
```

### List All Appointments (GET)
```bash
curl http://localhost:8000/appointments/
```

## 🛠️ Troubleshooting

### Docker not starting?
```bash
# Check if Docker Desktop is running
docker --version

# Check running containers
docker ps -a

# Restart container
docker-compose restart
```

### Database connection error?
```bash
# Check if PostgreSQL is running
docker ps

# Check logs
docker logs medical-ai-db

# Restart database
docker-compose down
docker-compose up -d
```

### Port 5432 already in use?
```bash
# Option 1: Stop other PostgreSQL instances
# Option 2: Change port in docker-compose.yml to "5433:5432"
# Then update DATABASE_URL in .env
```

### Error installing asyncpg on Windows?
```bash
# Install Microsoft C++ Build Tools
# Download from: https://visualstudio.microsoft.com/visual-cpp-build-tools/
```

## 🔄 Reset Database (if needed)

```bash
# Drop and recreate all tables
python init_db.py --drop
# Type 'yes' when prompted
```

## 🛑 Stop Everything

```bash
# Stop API server: Ctrl + C

# Stop Docker containers
docker-compose down

# Stop and remove data (careful!)
docker-compose down -v
```

## 📚 Next Steps

Once everything is running:
1. Read the API documentation at http://localhost:8000/docs
2. Test all endpoints using the interactive Swagger UI
3. Check [backend/README.md](README.md) for more details
4. Ready to add authentication? (Phase 3)
5. Ready to add AI? (Phase 4)

## ✅ Success Checklist

- [ ] Docker container running
- [ ] Virtual environment activated
- [ ] Dependencies installed
- [ ] Database tables created
- [ ] API server running on port 8000
- [ ] Can access http://localhost:8000/docs
- [ ] Can create users and appointments

If all boxes are checked, you're ready to go! 🎉
