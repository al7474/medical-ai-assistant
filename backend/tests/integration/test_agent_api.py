"""
Integration Tests for Agent API
Tests: agent chat, capabilities, tool execution
"""
import pytest  # type: ignore
from httpx import AsyncClient
from fastapi import status

pytestmark = pytest.mark.integration


class TestAgentAPI:
    """Test LangGraph agent endpoints"""
    
    @pytest.mark.asyncio
    async def test_get_agent_capabilities(self, async_client: AsyncClient, api_headers):
        """Test getting agent capabilities"""
        response = await async_client.get("/agent/capabilities", headers=api_headers)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "agent_available" in data
        assert "capabilities" in data
        assert isinstance(data["capabilities"], list)
        
        # Check tool names
        tool_names = [tool["name"] for tool in data["capabilities"]]
        assert "search_medical_documents" in tool_names
        assert "get_user_medical_profile" in tool_names
        assert "get_upcoming_appointments" in tool_names
    
    @pytest.mark.asyncio
    async def test_agent_chat_simple_query(self, async_client: AsyncClient, api_headers):
        """Test simple agent chat"""
        chat_data = {
            "message": "Hello, what can you help me with?",
            "use_context": False
        }
        
        response = await async_client.post(
            "/agent/chat",
            json=chat_data,
            headers=api_headers
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "response" in data
        assert isinstance(data["response"], str)
        assert len(data["response"]) > 0
    
    @pytest.mark.asyncio
    async def test_agent_chat_with_context(self, async_client: AsyncClient, api_headers, test_user_with_profile):
        """Test agent chat with medical context"""
        chat_data = {
            "message": "What are my current medications?",
            "use_context": True
        }
        
        response = await async_client.post(
            "/agent/chat",
            json=chat_data,
            headers=api_headers
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "response" in data
        # Should mention medications or use tools
        assert len(data["response"]) > 0
    
    @pytest.mark.asyncio
    async def test_test_tool_directly(self, async_client: AsyncClient, api_headers):
        """Test direct tool execution"""
        tool_params = {}
        
        response = await async_client.post(
            "/agent/test-tool/get_current_date_time",
            json=tool_params,
            headers=api_headers
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "result" in data
        assert "success" in data
    
    @pytest.mark.asyncio
    async def test_agent_requires_authentication(self, async_client: AsyncClient):
        """Test agent endpoints require authentication"""
        response = await async_client.get("/agent/capabilities")
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    @pytest.mark.asyncio
    @pytest.mark.slow
    async def test_agent_multi_step_reasoning(self, async_client: AsyncClient, api_headers, test_user_with_documents):
        """Test agent multi-step reasoning with tools"""
        chat_data = {
            "message": "Search my lab results for glucose levels and tell me if they're good",
            "use_context": True
        }
        
        response = await async_client.post(
            "/agent/chat",
            json=chat_data,
            headers=api_headers,
            timeout=30.0  # Agent may take longer
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "response" in data
        # Agent should use search tool and provide analysis
        assert len(data["response"]) > 50
