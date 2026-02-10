"""Test database connection"""
import asyncio
import asyncpg

async def test_connection():
    try:
        print("🔄 Testing direct asyncpg connection...")
        conn = await asyncpg.connect(
            host='127.0.0.1',
            port=5432,
            user='medical_user',
            password='medical_pass',
            database='medical_db'
        )
        print("✅ Connected successfully!")
        
        # Test query
        version = await conn.fetchval('SELECT version()')
        print(f"📊 PostgreSQL version: {version[:50]}...")
        
        await conn.close()
        print("✅ Connection closed successfully")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print(f"❌ Error type: {type(e).__name__}")

if __name__ == "__main__":
    asyncio.run(test_connection())
