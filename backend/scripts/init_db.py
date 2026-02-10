"""
Database Initialization Script
Run this script to create all database tables
Usage: python init_db.py
"""
import asyncio
from database import engine
from models import Base

async def init_db():
    """Create all database tables"""
    print("🔄 Connecting to database...")
    try:
        async with engine.begin() as conn:
            print("🔄 Creating tables...")
            await conn.run_sync(Base.metadata.create_all)
        print("✅ Database tables created successfully!")
        print("📋 Tables created: users, appointments")
    except Exception as e:
        print(f"❌ Error creating tables: {e}")
        raise

async def drop_all_tables():
    """Drop all database tables (USE WITH CAUTION!)"""
    print("⚠️  WARNING: Dropping all tables...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    print("✅ All tables dropped.")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--drop":
        print("⚠️  This will DELETE all tables and data!")
        confirm = input("Type 'yes' to confirm: ")
        if confirm.lower() == "yes":
            asyncio.run(drop_all_tables())
            asyncio.run(init_db())
        else:
            print("❌ Operation cancelled")
    else:
        asyncio.run(init_db())
