"""Test AI Chat functionality"""
import requests
import json

BASE_URL = "http://localhost:8000"

def test_info():
    """Check AI status"""
    print("🔍 Checking AI status...\n")
    response = requests.get(f"{BASE_URL}/info")
    data = response.json()
    
    ai_status = data.get("ai_status", {})
    print(f"AI Available: {ai_status.get('available')}")
    print(f"Provider: {ai_status.get('provider')}")
    print(f"Model: {ai_status.get('model')}")
    print(f"Setup Guide: {ai_status.get('setup_guide')}\n")
    
    return ai_status.get('available', False)

def test_chat(message: str):
    """Test chat endpoint"""
    print(f"💬 Sending: {message}")
    
    response = requests.post(
        f"{BASE_URL}/chat",
        json={"text": message}
    )
    
    if response.status_code == 200:
        data = response.json()
        print(f"🤖 Response: {data['bot_response']}")
        print(f"   AI Enabled: {data.get('ai_enabled', False)}")
        print(f"   Provider: {data.get('provider', 'unknown')}")
        print()
        return True
    else:
        print(f"❌ Error: {response.status_code}")
        print(f"   {response.text}\n")
        return False

def main():
    print("="*60)
    print("🧪 Medical AI Assistant - Chat Test")
    print("="*60)
    print()
    
    try:
        # Check AI status
        ai_available = test_info()
        
        if not ai_available:
            print("⚠️  AI is NOT enabled. Using fallback responses.")
            print("💡 To enable AI:")
            print("   1. Get API key from https://platform.openai.com/api-keys")
            print("   2. Add to .env: OPENAI_API_KEY=sk-...")
            print("   3. Restart server\n")
        else:
            print("✅ AI is ENABLED! Testing with real AI...\n")
        
        # Test messages
        test_messages = [
            "Hello!",
            "I have a headache for 3 days. What should I do?",
            "Can you help me schedule an appointment?"
        ]
        
        print("="*60)
        print("📝 Testing Chat Messages")
        print("="*60)
        print()
        
        for msg in test_messages:
            test_chat(msg)
            print("-"*60)
        
        print("\n✅ All tests completed!")
        
        if ai_available:
            print("\n🎉 Your AI is working perfectly!")
        else:
            print("\n💡 Add an API key to unlock AI features!")
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to API.")
        print("   Make sure the server is running:")
        print("   python -m uvicorn main:app --reload")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
