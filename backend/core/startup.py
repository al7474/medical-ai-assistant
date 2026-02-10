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
        return True
    except OperationalError as e:
        print(f"⚠️  Database connection failed: {e}")
        print("⚠️  Server will start but database operations will fail")
        print("⚠️  Make sure DATABASE_URL is correct and database is accessible")
        return False
    except Exception as e:
        print(f"⚠️  Unexpected error during database initialization: {e}")
        print("⚠️  Server will start but database operations may fail")
        return False


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup and shutdown events"""
    # Startup - don't fail if database is not ready
    await init_database()
    yield
    # Shutdown
    print("👋 Shutting down...")
