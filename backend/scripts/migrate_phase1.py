"""
Database Migration Script - Phase 1: Medical Data Models
Migrates the database to add:
- medical_profiles
- conversations
- messages
- medical_documents

Usage: python scripts/migrate_phase1.py
"""
import sys
import os
from pathlib import Path

# Add parent directory to path to import modules
sys.path.insert(0, str(Path(__file__).parent.parent))

import asyncio
from database import engine
from models import Base
from sqlalchemy import text


async def main():
    """Main migration function"""
    print("╔═══════════════════════════════════════════╗")
    print("║   Medical AI Assistant - Database Migration   ║")
    print("║              Phase 1: Medical Data             ║")
    print("╚═══════════════════════════════════════════╝\n")
    
    print("🔄 Phase 1 Migration: Medical Data Models")
    print("=" * 50)
    
    try:
        async with engine.begin() as conn:
            print("🔄 Connecting to database...")
            
            # Check current state
            result = await conn.execute(text("SELECT COUNT(*) FROM users"))
            user_count = result.scalar()
            print(f"📊 Current users: {user_count}")
            
            # Create all tables (will skip existing ones)
            print("\n🔄 Creating new tables...")
            await conn.run_sync(Base.metadata.create_all)
            
            # Verify new tables exist
            print("\n✅ Verifying tables...")
            result = await conn.execute(text("""
                SELECT tablename 
                FROM pg_tables 
                WHERE schemaname = 'public'
                ORDER BY tablename
            """))
            
            tables = [row[0] for row in result.fetchall()]
            
            print("\n📋 Current tables in database:")
            for table in tables:
                print(f"  ✓ {table}")
            
            # Check for new tables
            new_tables = ["medical_profiles", "conversations", "messages", "medical_documents"]
            print("\n🎯 New tables added:")
            for table in new_tables:
                if table in tables:
                    print(f"  ✅ {table}")
                else:
                    print(f"  ❌ {table} (NOT FOUND)")
            
        print("\n" + "=" * 50)
        print("✅ Migration completed successfully!")
        print("\n💡 Next steps:")
        print("  1. Restart your backend server")
        print("  2. Test the new endpoints:")
        print("     - POST /medical-profile/")
        print("     - GET  /medical-profile/me")
        print("     - GET  /conversations/")
        print("  3. Check API docs: http://localhost:8000/docs")
        
    except Exception as e:
        print(f"\n❌ Migration error: {e}")
        import traceback
        traceback.print_exc()
        raise


if __name__ == "__main__":
    asyncio.run(main())
