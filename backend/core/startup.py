"""
Startup event handlers for FastAPI
Ensures database is ready before handling requests
"""
from contextlib import asynccontextmanager
from fastapi import FastAPI
from sqlalchemy.exc import OperationalError
import models
import database


async def init_database():
    """Initialize database tables if they don't exist"""
    try:
        print("🔄 Checking database connection...")
        async with database.engine.begin() as conn:
            print("🔄 Creating tables if they don't exist...")
            await conn.run_sync(models.Base.metadata.create_all)
        print("✅ Database ready!")
    except OperationalError as e:
        print(f"❌ Database connection failed: {e}")
        print("⚠️  Make sure PostgreSQL is running (docker-compose up -d)")
        raise
    except Exception as e:
        print(f"❌ Unexpected error during database initialization: {e}")
        raise


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup and shutdown events"""
    # Startup
    await init_database()
    yield
    # Shutdown
    print("👋 Shutting down...")
