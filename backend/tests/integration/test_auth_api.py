"""
Integration Tests for Authentication API
Tests: register, login, token validation
"""
import pytest  # type: ignore
from httpx import AsyncClient
from fastapi import status

pytestmark = pytest.mark.integration


class TestAuthenticationAPI:
    """Test authentication endpoints"""
    
    @pytest.mark.asyncio
    async def test_register_new_user(self, async_client: AsyncClient):
        """Test successful user registration"""
        user_data = {
            "name": "New User",
            "email": "newuser@example.com",
            "password": "SecurePass123!"
        }
        
        response = await async_client.post("/auth/register", json=user_data)
        
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["email"] == user_data["email"]
        assert data["name"] == user_data["name"]
        assert "id" in data
    
    @pytest.mark.asyncio
    async def test_register_duplicate_email(self, async_client: AsyncClient, test_user):
        """Test registration with existing email fails"""
        user_data = {
            "name": "Duplicate User",
            "email": test_user.email,
            "password": "Password123!"
        }
        
        response = await async_client.post("/auth/register", json=user_data)
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
    
    @pytest.mark.asyncio
    async def test_login_success(self, async_client: AsyncClient, test_user):
        """Test successful login"""
        login_data = {
            "username": test_user.email,
            "password": "testpass123"
        }
        
        response = await async_client.post("/auth/login", data=login_data)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
    
    @pytest.mark.asyncio
    async def test_login_invalid_credentials(self, async_client: AsyncClient):
        """Test login with invalid credentials"""
        login_data = {
            "username": "nonexistent@example.com",
            "password": "wrongpassword"
        }
        
        response = await async_client.post("/auth/login", data=login_data)
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    @pytest.mark.asyncio
    async def test_get_current_user(self, async_client: AsyncClient, api_headers, test_user):
        """Test getting current authenticated user"""
        response = await async_client.get("/auth/me", headers=api_headers)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["email"] == test_user.email
    
    @pytest.mark.asyncio
    async def test_protected_endpoint_without_token(self, async_client: AsyncClient):
        """Test protected endpoint returns 401 without token"""
        response = await async_client.get("/auth/me")
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
