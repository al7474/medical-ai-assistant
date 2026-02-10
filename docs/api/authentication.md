# 🔐 Authentication System - JWT

## Overview

The Medical AI Assistant now includes a complete JWT (JSON Web Token) authentication system implemented in Phase 5. This provides secure user authentication and authorization for accessing protected endpoints.

## Features Implemented

✅ **User Registration** - Create new user accounts with hashed passwords  
✅ **User Login** - Authenticate and receive JWT access tokens  
✅ **Token Validation** - Secure middleware to validate tokens  
✅ **Protected Routes** - Endpoints that require authentication  
✅ **Password Hashing** - Secure password storage with bcrypt  
✅ **Token Expiration** - Tokens expire after 7 days by default  

## Architecture

### Components

```
services/
  └── auth_service.py     # Password hashing and JWT operations
  
schemas/
  └── auth.py             # Authentication Pydantic models
  
api/
  ├── deps.py             # Authentication dependencies
  └── routes/
      └── auth.py         # Authentication endpoints
      
models/
  └── user.py             # Extended User model with auth fields
```

### User Model Updates

The `User` model now includes:

```python
class User(Base):
    id               # Primary key
    name             # User's full name
    email            # Unique email address
    password_hash    # Hashed password (never stored in plain text)
    is_active        # Account status flag
    created_at       # Registration timestamp
    updated_at       # Last modification timestamp
```

## API Endpoints

### 1. Register New User

**Endpoint:** `POST /auth/register`

**Request Body:**
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "password": "SecurePassword123!"
}
```

**Response:** `201 Created`
```json
{
  "id": 1,
  "name": "John Doe",
  "email": "john@example.com",
  "is_active": true,
  "created_at": "2026-02-10T02:41:39.621222"
}
```

**Validations:**
- Email must be valid format
- Email must be unique
- Password is hashed before storing

---

### 2. Login

**Endpoint:** `POST /auth/login`

**Request Body:** (form data, not JSON)
```
username: john@example.com  # Note: OAuth2 spec requires 'username' field
password: SecurePassword123!
```

**Response:** `200 OK`
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Usage:**
- Returns a JWT token valid for 7 days
- Use this token in Authorization header for protected endpoints

---

### 3. Get Current User Info

**Endpoint:** `GET /auth/me`

**Headers:**
```
Authorization: Bearer <your_token_here>
```

**Response:** `200 OK`
```json
{
  "id": 1,
  "name": "John Doe",
  "email": "john@example.com",
  "is_active": true,
  "created_at": "2026-02-10T02:41:39.621222"
}
```

**Protected:** ✅ Requires valid JWT token

---

### 4. Logout

**Endpoint:** `POST /auth/logout`

**Response:** `200 OK`
```json
{
  "message": "Successfully logged out",
  "detail": "Please remove the token from your client storage"
}
```

**Note:** JWT tokens are stateless, so logout is handled client-side by discarding the token

## Using Authentication

### In Swagger UI (http://localhost:8000/docs)

1. **Register a user:**
   - Click on `POST /auth/register`
   - Click "Try it out"
   - Fill in the user data
   - Execute

2. **Login:**
   - Click on `POST /auth/login`
   - Click "Try it out"
   - Enter email in `username` field (OAuth2 requirement)
   - Enter password
   - Execute
   - Copy the `access_token` from response

3. **Authorize:**
   - Click the **"Authorize"** button at the top
   - Paste your token in the value field
   - Click "Authorize"
   - Click "Close"

4. **Access protected endpoints:**
   - Now you can access `/auth/me` and any other protected endpoints

### In Python Code

```python
import requests

# 1. Register
register_data = {
    "name": "John Doe",
    "email": "john@example.com",
    "password": "SecurePass123!"
}
response = requests.post(
    "http://localhost:8000/auth/register",
    json=register_data
)
print(response.json())

# 2. Login
login_data = {
    "username": "john@example.com",  # OAuth2 requires 'username'
    "password": "SecurePass123!"
}
response = requests.post(
    "http://localhost:8000/auth/login",
    data=login_data  # Note: form data, not json
)
token = response.json()["access_token"]

# 3. Use token for protected endpoints
headers = {"Authorization": f"Bearer {token}"}
response = requests.get(
    "http://localhost:8000/auth/me",
    headers=headers
)
print(response.json())
```

### In JavaScript/Frontend

```javascript
// 1. Register
const registerResponse = await fetch('http://localhost:8000/auth/register', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    name: 'John Doe',
    email: 'john@example.com',
    password: 'SecurePass123!'
  })
});
const user = await registerResponse.json();

// 2. Login
const loginResponse = await fetch('http://localhost:8000/auth/login', {
  method: 'POST',
  headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
  body: new URLSearchParams({
    username: 'john@example.com',  // OAuth2 requires 'username'
    password: 'SecurePass123!'
  })
});
const { access_token } = await loginResponse.json();

// 3. Save token (localStorage, sessionStorage, or cookie)
localStorage.setItem('token', access_token);

// 4. Use token for protected endpoints
const response = await fetch('http://localhost:8000/auth/me', {
  headers: {
    'Authorization': `Bearer ${localStorage.getItem('token')}`
  }
});
const currentUser = await response.json();
```

## Security Configuration

### Environment Variables

Add to your `.env` file:

```env
# JWT Configuration
SECRET_KEY=your-secret-key-change-in-production-please-use-openssl-rand-hex-32
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=10080  # 7 days
```

### Generate Secure Secret Key

```bash
# Using OpenSSL
openssl rand -hex 32

# Using Python
python -c "import secrets; print(secrets.token_hex(32))"
```

**⚠️ IMPORTANT:** Always use a strong, unique secret key in production!

## Protecting Your Endpoints

### Make an endpoint require authentication:

```python
from fastapi import APIRouter, Depends
from models import User
from api.deps import get_current_active_user

router = APIRouter()

@router.get("/protected-route")
async def protected_route(
    current_user: User = Depends(get_current_active_user)
):
    """
    This endpoint requires authentication.
    current_user will contain the authenticated user's data
    """
    return {
        "message": f"Hello {current_user.name}!",
        "user_id": current_user.id
    }
```

### Dependencies Available:

1. **`get_current_user`** - Get any authenticated user
2. **`get_current_active_user`** - Get only active users (recommended)

## Error Responses

### 401 Unauthorized

```json
{
  "detail": "Could not validate credentials"
}
```

**Causes:**
- Token is missing
- Token is invalid
- Token is expired
- User doesn't exist

### 400 Bad Request

```json
{
  "detail": "Email already registered"
}
```

**Causes:**
- Email already exists during registration
- Invalid email format
- User account is inactive

### 422 Validation Error

```json
{
  "detail": [
    {
      "loc": ["body", "email"],
      "msg": "Invalid email format",
      "type": "value_error"
    }
  ]
}
```

**Causes:**
- Invalid request data
- Missing required fields
- Wrong data types

## Testing

### Automated Test Script

Run the included test script:

```bash
python test_auth.py
```

**Tests:**
- ✅ User registration
- ✅ User login
- ✅ Get current user info with valid token
- ✅ Access denied without token
- ✅ Access denied with invalid token

### Manual Testing

1. Start the server: `uvicorn main:app --reload`
2. Open Swagger UI: http://localhost:8000/docs
3. Follow the "Using Authentication" steps above

## Token Lifecycle

```
1. User registers     → Password hashed and stored
2. User logs in       → JWT token generated (expires in 7 days)
3. Client stores token → localStorage/cookie
4. Each request       → Token sent in Authorization header
5. Server validates   → Extracts user from token
6. Access granted     → User can access protected resources
7. Token expires      → User must login again
```

## Security Best Practices

✅ **Implemented:**
- Passwords are hashed with bcrypt
- JWT tokens with expiration
- Secure token validation
- HTTPS recommended in production
- Unique email addresses enforced

⚠️ **Production Recommendations:**
- Use strong SECRET_KEY (32+ random bytes)
- Enable HTTPS only
- Consider adding refresh tokens
- Implement rate limiting
- Add account lockout after failed attempts
- Enable email verification
- Add 2FA (Two-Factor Authentication)
- Implement password reset functionality

## Next Steps

Ready to enhance authentication:

1. **Email Verification** - Verify user emails during registration
2. **Password Reset** - Allow users to reset forgotten passwords
3. **Refresh Tokens** - Implement token refresh mechanism
4. **Role-Based Access** - Add user roles (admin, doctor, patient)
5. **2FA** - Add two-factor authentication
6. **OAuth2** - Social login (Google, GitHub, etc.)
7. **Account Management** - Update profile, change password

## Dependencies Added

```
python-jose[cryptography]==3.3.0  # JWT encoding/decoding
passlib[bcrypt]==1.7.4            # Password hashing
bcrypt==4.0.1                     # Hashing algorithm
email-validator==2.3.0            # Email validation
```

---

**Phase 5 Complete! 🎉**

*Current Progress: ~75%  
Next: Frontend Development or WebSocket Integration*
