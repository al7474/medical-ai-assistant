"""Test with psycopg2"""
import psycopg2

try:
    print("🔄 Testing psycopg2 connection...")
    conn = psycopg2.connect(
        host='127.0.0.1',
        port=5433,
        user='medical_user',
        password='medical_pass',
        database='medical_db'
    )
    print("✅ Connected successfully!")
    
    cur = conn.cursor()
    cur.execute('SELECT version()')
    version = cur.fetchone()
    print(f"📊 PostgreSQL version: {version[0][:50]}...")
    
    cur.close()
    conn.close()
    print("✅ Connection closed")
    
except Exception as e:
    print(f"❌ Error: {e}")
    print(f"❌ Error type: {type(e).__name__}")
