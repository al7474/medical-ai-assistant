"""
Test Authentication Endpoints
Tests register, login, and protected routes
"""
import requests
import json


BASE_URL = "http://localhost:8000"


def test_register():
    """Test user registration"""
    print("\n🧪 Testing User Registration...")
    
    user_data = {
        "name": "Test User",
        "email": "test@example.com",
        "password": "TestPassword123!"
    }
    
    response = requests.post(f"{BASE_URL}/auth/register", json=user_data)
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    if response.status_code == 201:
        print("✅ Registration successful!")
        return response.json()
    else:
        print("❌ Registration failed!")
        return None


def test_login(email: str, password: str):
    """Test user login"""
    print("\n🧪 Testing User Login...")
    
    # OAuth2PasswordRequestForm requires form data, not JSON
    login_data = {
        "username": email,  # OAuth2 spec requires 'username' field
        "password": password
    }
    
    response = requests.post(f"{BASE_URL}/auth/login", data=login_data)
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    if response.status_code == 200:
        print("✅ Login successful!")
        return response.json()["access_token"]
    else:
        print("❌ Login failed!")
        return None


def test_get_current_user(token: str):
    """Test getting current user info"""
    print("\n🧪 Testing Get Current User...")
    
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    response = requests.get(f"{BASE_URL}/auth/me", headers=headers)
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    if response.status_code == 200:
        print("✅ Get current user successful!")
        return response.json()
    else:
        print("❌ Get current user failed!")
        return None


def test_protected_endpoint_without_token():
    """Test accessing protected endpoint without token"""
    print("\n🧪 Testing Protected Endpoint Without Token...")
    
    response = requests.get(f"{BASE_URL}/auth/me")
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    if response.status_code == 401:
        print("✅ Correctly denied access without token!")
    else:
        print("❌ Should have been denied!")


def test_invalid_token():
    """Test using invalid token"""
    print("\n🧪 Testing Invalid Token...")
    
    headers = {
        "Authorization": "Bearer invalid_token_here"
    }
    
    response = requests.get(f"{BASE_URL}/auth/me", headers=headers)
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    if response.status_code == 401:
        print("✅ Correctly rejected invalid token!")
    else:
        print("❌ Should have been rejected!")


def run_all_tests():
    """Run all authentication tests"""
    print("=" * 60)
    print(" 🔐 AUTHENTICATION SYSTEM TESTS")
    print("=" * 60)
    
    # Test 1: Register a new user
    user = test_register()
    
    if not user:
        print("\n⚠️  Cannot continue tests without successful registration")
        print("Note: If user already exists, try with a different email")
        return
    
    # Test 2: Login with the registered user
    token = test_login("test@example.com", "TestPassword123!")
    
    if not token:
        print("\n⚠️  Cannot continue tests without successful login")
        return
    
    # Test 3: Get current user info with valid token
    test_get_current_user(token)
    
    # Test 4: Try to access protected endpoint without token
    test_protected_endpoint_without_token()
    
    # Test 5: Try to access with invalid token
    test_invalid_token()
    
    print("\n" + "=" * 60)
    print(" ✅ ALL TESTS COMPLETED!")
    print("=" * 60)
    print("\n💡 Tips:")
    print("  - View all endpoints at: http://localhost:8000/docs")
    print("  - Use the token in Swagger UI to test other protected endpoints")
    print("  - Token expires in 7 days by default")


if __name__ == "__main__":
    try:
        run_all_tests()
    except requests.exceptions.ConnectionError:
        print("❌ ERROR: Cannot connect to server")
        print("Make sure the server is running: uvicorn main:app --reload")
    except Exception as e:
        print(f"❌ ERROR: {e}")
