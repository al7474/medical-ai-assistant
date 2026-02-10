"""
WebSocket Chat Client - Test Script
Tests real-time chat with authentication
"""
import asyncio
import websockets
import json
import requests
from datetime import datetime


BASE_URL = "http://localhost:8000"
WS_URL = "ws://localhost:8000"


def register_and_login():
    """Register a new user and get JWT token"""
    print("\n🔐 Registering and logging in...")
    
    # Try to register (might fail if user exists)
    register_data = {
        "name": "WebSocket Test User",
        "email": "wstest@example.com",
        "password": "TestWS123!"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/register", json=register_data)
        if response.status_code == 201:
            print("✅ User registered successfully")
        elif response.status_code == 400:
            print("ℹ️  User already exists, continuing with login...")
    except Exception as e:
        print(f"⚠️  Registration note: {e}")
    
    # Login
    login_data = {
        "username": "wstest@example.com",
        "password": "TestWS123!"
    }
    
    response = requests.post(f"{BASE_URL}/auth/login", data=login_data)
    
    if response.status_code == 200:
        token = response.json()["access_token"]
        print(f"✅ Login successful!")
        print(f"📝 Token: {token[:50]}...")
        return token
    else:
        print(f"❌ Login failed: {response.json()}")
        return None


async def websocket_chat_test(token):
    """Test WebSocket chat functionality"""
    print("\n🌐 Connecting to WebSocket...")
    
    uri = f"{WS_URL}/ws/chat?token={token}"
    
    try:
        async with websockets.connect(uri) as websocket:
            print("✅ Connected to WebSocket!")
            
            # Receive welcome message
            welcome = await websocket.recv()
            welcome_data = json.loads(welcome)
            print(f"\n📨 Received: {welcome_data['type']} - {welcome_data['message']}")
            
            # Test messages
            test_messages = [
                "Hello! Can you help me?",
                "What should I do if I have a headache?",
                "Thanks for your help!"
            ]
            
            for i, message in enumerate(test_messages, 1):
                print(f"\n{'='*60}")
                print(f"Test {i}/{len(test_messages)}")
                print(f"{'='*60}")
                
                # Send message
                print(f"📤 Sending: {message}")
                await websocket.send(json.dumps({
                    "type": "message",
                    "text": message,
                    "context": {
                        "test_number": i
                    }
                }))
                
                # Receive typing indicator
                try:
                    typing = await asyncio.wait_for(websocket.recv(), timeout=2.0)
                    typing_data = json.loads(typing)
                    if typing_data.get('type') == 'typing':
                        print(f"⏳ {typing_data.get('message', 'AI is typing...')}")
                except asyncio.TimeoutError:
                    print("⏳ Waiting for response...")
                
                # Receive response
                response = await websocket.recv()
                response_data = json.loads(response)
                
                print(f"📨 Response type: {response_data['type']}")
                print(f"🤖 AI: {response_data.get('text', 'No response')}")
                print(f"⚙️  Provider: {response_data.get('provider', 'unknown')}")
                print(f"🔧 Model: {response_data.get('model', 'unknown')}")
                print(f"🕐 Timestamp: {response_data.get('timestamp', 'N/A')}")
                
                # Small delay between messages
                await asyncio.sleep(1)
            
            print(f"\n{'='*60}")
            print("✅ All test messages completed successfully!")
            print(f"{'='*60}")
            
    except websockets.exceptions.InvalidStatusCode as e:
        print(f"❌ Connection failed: {e}")
        print("💡 Make sure:")
        print("   1. Server is running (uvicorn main:app --reload)")
        print("   2. Token is valid (not expired)")
        print("   3. User account is active")
    except Exception as e:
        print(f"❌ Error: {e}")


async def test_active_users():
    """Test getting active users endpoint"""
    print("\n👥 Checking active users...")
    
    try:
        response = requests.get(f"{BASE_URL}/ws/active-users")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Active users: {len(data['active_users'])}")
            print(f"✅ Total connections: {data['total_connections']}")
            
            for user in data['active_users']:
                print(f"   - {user['user_name']} (ID: {user['user_id']}) - {user['connections']} connection(s)")
        else:
            print(f"❌ Failed to get active users: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")


async def main():
    """Run all WebSocket tests"""
    print("=" * 60)
    print(" 🌐 WEBSOCKET REAL-TIME CHAT TESTS")
    print("=" * 60)
    
    # Get token
    token = register_and_login()
    
    if not token:
        print("\n❌ Cannot continue without token")
        return
    
    # Test WebSocket chat
    await websocket_chat_test(token)
    
    # Check active users
    await test_active_users()
    
    print("\n" + "=" * 60)
    print(" ✅ ALL WEBSOCKET TESTS COMPLETED!")
    print("=" * 60)
    print("\n💡 Tips:")
    print("  - Open the HTML test client: http://localhost:8000/ws/test-client")
    print("  - Use your token from login to connect")
    print("  - Multiple users can connect simultaneously")
    print("  - Messages are processed in real-time with AI")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n⚠️  Test interrupted by user")
    except requests.exceptions.ConnectionError:
        print("❌ ERROR: Cannot connect to server")
        print("Make sure the server is running: uvicorn main:app --reload")
    except Exception as e:
        print(f"❌ ERROR: {e}")
