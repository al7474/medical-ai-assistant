"""
Integration Tests for WebSocket Chat
Tests: connection, messaging, agent mode
"""
import pytest  # type: ignore
from httpx import AsyncClient
import asyncio

pytestmark = pytest.mark.integration


class TestWebSocketChat:
    """Test WebSocket chat functionality"""
    
    @pytest.mark.asyncio
    async def test_websocket_connection(self, websocket_client):
        """Test WebSocket connection with authentication"""
        async with websocket_client as ws:
            # Test connection established
            assert ws.client_state.name == "CONNECTED"
    
    @pytest.mark.asyncio
    async def test_websocket_authentication(self, websocket_client, authenticated_user):
        """Test WebSocket authentication"""
        _, token = authenticated_user
        
        async with websocket_client as ws:
            # Send auth message
            await ws.send_json({
                "type": "auth",
                "token": token
            })
            
            # Should receive confirmation
            response = await ws.receive_json()
            assert response["type"] == "auth_success"
    
    @pytest.mark.asyncio
    async def test_websocket_simple_message(self, websocket_client, authenticated_user):
        """Test sending simple chat message"""
        _, token = authenticated_user
        
        async with websocket_client as ws:
            # Authenticate
            await ws.send_json({"type": "auth", "token": token})
            await ws.receive_json()  # auth confirmation
            
            # Send message
            await ws.send_json({
                "type": "message",
                "text": "Hello, how are you?",
                "use_agent": False
            })
            
            # Should receive typing indicator
            response = await ws.receive_json()
            assert response["type"] in ["typing", "message"]
            
            # Should receive response
            if response["type"] == "typing":
                response = await ws.receive_json()
            
            assert response["type"] == "message"
            assert "text" in response
    
    @pytest.mark.asyncio
    @pytest.mark.slow
    async def test_websocket_agent_mode(self, websocket_client, authenticated_user):
        """Test WebSocket with agent mode enabled"""
        _, token = authenticated_user
        
        async with websocket_client as ws:
            # Authenticate
            await ws.send_json({"type": "auth", "token": token})
            await ws.receive_json()
            
            # Send message with agent enabled
            await ws.send_json({
                "type": "message",
                "text": "What is today's date?",
                "use_agent": True,
                "use_context": False
            })
            
            # Wait for response (may take longer with agent)
            response = await asyncio.wait_for(
                ws.receive_json(),
                timeout=30.0
            )
            
            assert response["type"] in ["typing", "message"]
            if response["type"] == "typing":
                response = await ws.receive_json()
            
            assert response["type"] == "message"
            assert "mode" in response
            assert response["mode"] == "agent"
    
    @pytest.mark.asyncio
    async def test_websocket_invalid_token(self, websocket_client):
        """Test WebSocket with invalid token"""
        async with websocket_client as ws:
            # Send invalid auth
            await ws.send_json({
                "type": "auth",
                "token": "invalid_token_123"
            })
            
            # Should receive error
            response = await ws.receive_json()
            assert response["type"] == "error"
