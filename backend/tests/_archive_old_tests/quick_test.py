"""Quick API test"""
import requests

print("🧪 Testing API endpoints...\n")

# Test stats endpoint
try:
    response = requests.get("http://localhost:8000/stats")
    if response.status_code == 200:
        print("✅ /stats endpoint working!")
        print(f"📊 Response: {response.json()}\n")
    else:
        print(f"❌ Stats endpoint returned: {response.status_code}")
except requests.exceptions.ConnectionError:
    print("❌ Cannot connect to API. Is it running?")
except Exception as e:
    print(f"❌ Error: {e}")

# Test health endpoint
try:
    response = requests.get("http://localhost:8000/health")
    if response.status_code == 200:
        print("✅ /health endpoint working!")
        print(f"💚 Response: {response.json()}\n")
except Exception as e:
    print(f"❌ Health check failed: {e}")

print("✅ All tests completed!")
