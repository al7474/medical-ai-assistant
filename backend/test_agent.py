"""
Test script for LangGraph Agent
Demonstrates agent capabilities with examples
"""

import requests
import json
from typing import Optional

# Configuration
BASE_URL = "http://localhost:8000"
# Replace with your JWT token after logging in
JWT_TOKEN = "YOUR_JWT_TOKEN_HERE"

headers = {
    "Authorization": f"Bearer {JWT_TOKEN}",
    "Content-Type": "application/json"
}


def test_agent_capabilities():
    """Get available agent tools"""
    print("\n" + "="*60)
    print("🔍 Testing: Get Agent Capabilities")
    print("="*60)
    
    response = requests.get(
        f"{BASE_URL}/agent/capabilities",
        headers=headers
    )
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Agent Available: {data['agent_available']}")
        print(f"🤖 Provider: {data['provider']}")
        print(f"\n📋 Available Tools ({len(data['capabilities'])}):")
        for tool in data['capabilities']:
            print(f"  - {tool['name']}: {tool['description'][:80]}...")
    else:
        print(f"❌ Error: {response.status_code}")
        print(response.text)


def test_agent_chat(message: str, use_context: bool = True):
    """Test agent chat endpoint"""
    print("\n" + "="*60)
    print(f"💬 Testing: Agent Chat")
    print("="*60)
    print(f"📝 User: {message}")
    
    response = requests.post(
        f"{BASE_URL}/agent/chat",
        headers=headers,
        json={
            "message": message,
            "use_context": use_context
        }
    )
    
    if response.status_code == 200:
        data = response.json()
        print(f"🤖 Agent: {data['response']}")
        print(f"💾 Conversation ID: {data['conversation_id']}")
    else:
        print(f"❌ Error: {response.status_code}")
        print(response.text)


def test_tool_directly(tool_name: str, parameters: dict):
    """Test individual tool"""
    print("\n" + "="*60)
    print(f"🔧 Testing Tool: {tool_name}")
    print("="*60)
    print(f"📋 Parameters: {json.dumps(parameters, indent=2)}")
    
    response = requests.post(
        f"{BASE_URL}/agent/test-tool/{tool_name}",
        headers=headers,
        json=parameters
    )
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Result:")
        print(data['result'])
    else:
        print(f"❌ Error: {response.status_code}")
        print(response.text)


def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("🎯 LangGraph Agent Test Suite")
    print("="*60)
    
    # Check if token is configured
    if JWT_TOKEN == "YOUR_JWT_TOKEN_HERE":
        print("\n⚠️  WARNING: JWT_TOKEN not configured!")
        print("📝 Steps to get your token:")
        print("   1. POST to /auth/login with your credentials")
        print("   2. Copy the 'access_token' from response")
        print("   3. Update JWT_TOKEN in this script")
        print("   4. Run again")
        return
    
    # Test 1: Agent capabilities
    test_agent_capabilities()
    
    # Test 2: Tool - Get current date/time
    test_tool_directly(
        "get_current_date_time",
        {}
    )
    
    # Test 3: Tool - Get medical profile
    test_tool_directly(
        "get_user_medical_profile",
        {}
    )
    
    # Test 4: Tool - List documents
    test_tool_directly(
        "list_medical_documents",
        {"limit": 5}
    )
    
    # Test 5: Agent chat - Simple query
    test_agent_chat(
        "What is today's date?"
    )
    
    # Test 6: Agent chat - Complex multi-tool query
    test_agent_chat(
        "Do I have any upcoming appointments? Also, what documents do I have uploaded?"
    )
    
    # Test 7: Agent chat - Document search
    test_agent_chat(
        "Search my medical documents for any mentions of blood pressure"
    )
    
    # Test 8: Agent chat - Appointment scheduling
    test_agent_chat(
        "I need to schedule a cardiology appointment for next Monday at 2 PM with Dr. Smith"
    )
    
    print("\n" + "="*60)
    print("✅ Test Suite Complete!")
    print("="*60)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
