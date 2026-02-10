"""
WebSocket endpoints for real-time chat
"""
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Query, Depends, status
from fastapi.responses import HTMLResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import Optional
import json
from datetime import datetime

from models import User
from services.websocket_manager import get_connection_manager
from services.chat_service import get_chat_service
from services.auth_service import verify_token
from api.deps import get_db


router = APIRouter(prefix="/ws", tags=["websocket"])


async def get_user_from_token(
    token: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_db)
) -> Optional[User]:
    """
    Get user from JWT token (for WebSocket authentication)
    
    Args:
        token: JWT token from query parameter
        db: Database session
        
    Returns:
        User object if valid, None otherwise
    """
    if not token:
        return None
    
    # Verify token
    email = verify_token(token)
    if not email:
        return None
    
    # Get user from database
    result = await db.execute(select(User).where(User.email == email))
    user = result.scalar_one_or_none()
    
    return user


@router.websocket("/chat")
async def websocket_chat(
    websocket: WebSocket,
    token: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_db)
):
    """
    WebSocket endpoint for real-time chat with AI assistant
    
    Connection URL: ws://localhost:8000/ws/chat?token=YOUR_JWT_TOKEN
    
    **Authentication:**
    - Requires valid JWT token in query parameter
    - Token must be from /auth/login endpoint
    
    **Message Format (Client → Server):**
    ```json
    {
        "type": "message",
        "text": "Your message here",
        "context": {}  // Optional context
    }
    ```
    
    **Message Format (Server → Client):**
    ```json
    {
        "type": "message",
        "text": "AI response",
        "user_message": "Your message",
        "timestamp": "2026-02-10T03:00:00",
        "ai_enabled": true,
        "provider": "openai"
    }
    ```
    
    **System Messages:**
    ```json
    {
        "type": "system",
        "message": "Connected successfully",
        "user": {"id": 1, "name": "John"}
    }
    ```
    
    **Error Messages:**
    ```json
    {
        "type": "error",
        "message": "Error description"
    }
    ```
    """
    manager = get_connection_manager()
    
    # Authenticate user
    user = await get_user_from_token(token, db)
    
    if not user:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return
    
    if not user.is_active:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return
    
    # Connect user
    await manager.connect(websocket, user.id, user.name)
    
    # Send welcome message
    await manager.send_personal_message(
        {
            "type": "system",
            "message": f"Welcome {user.name}! Connected to AI Medical Assistant",
            "user": {
                "id": user.id,
                "name": user.name,
                "email": user.email
            },
            "timestamp": datetime.utcnow().isoformat()
        },
        websocket
    )
    
    # Get AI service
    chat_service = get_chat_service()
    
    try:
        while True:
            # Receive message from client
            data = await websocket.receive_text()
            
            try:
                message_data = json.loads(data)
            except json.JSONDecodeError:
                await manager.send_personal_message(
                    {
                        "type": "error",
                        "message": "Invalid JSON format",
                        "timestamp": datetime.utcnow().isoformat()
                    },
                    websocket
                )
                continue
            
            # Extract message details
            message_type = message_data.get("type", "message")
            user_message = message_data.get("text", "")
            context = message_data.get("context", {})
            
            if not user_message:
                await manager.send_personal_message(
                    {
                        "type": "error",
                        "message": "Message text is required",
                        "timestamp": datetime.utcnow().isoformat()
                    },
                    websocket
                )
                continue
            
            # Add user info to context
            context.update({
                "user_id": user.id,
                "user_name": user.name,
                "user_email": user.email
            })
            
            # Send typing indicator
            await manager.send_personal_message(
                {
                    "type": "typing",
                    "message": "AI is thinking...",
                    "timestamp": datetime.utcnow().isoformat()
                },
                websocket
            )
            
            # Get AI response
            try:
                bot_response = await chat_service.chat(user_message, context)
            except Exception as e:
                bot_response = f"Sorry, I encountered an error: {str(e)}"
            
            # Send response
            await manager.send_personal_message(
                {
                    "type": "message",
                    "text": bot_response,
                    "user_message": user_message,
                    "timestamp": datetime.utcnow().isoformat(),
                    "ai_enabled": chat_service.is_available(),
                    "provider": chat_service.provider if chat_service.is_available() else "fallback",
                    "model": chat_service.model_name if chat_service.is_available() else "simple"
                },
                websocket
            )
            
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception as e:
        print(f"❌ WebSocket error: {e}")
        manager.disconnect(websocket)


@router.get("/active-users")
async def get_active_users():
    """
    Get list of currently active WebSocket users
    
    Returns list of connected users with their connection info
    """
    manager = get_connection_manager()
    return {
        "active_users": manager.get_active_users(),
        "total_connections": manager.get_total_connections()
    }


@router.get("/test-client")
async def get_test_client():
    """
    Simple HTML WebSocket test client
    
    Access at: http://localhost:8000/ws/test-client
    """
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>WebSocket Chat Test Client</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                max-width: 800px;
                margin: 50px auto;
                padding: 20px;
                background-color: #f5f5f5;
            }
            .container {
                background: white;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }
            h1 {
                color: #333;
                border-bottom: 2px solid #4CAF50;
                padding-bottom: 10px;
            }
            .status {
                padding: 10px;
                border-radius: 5px;
                margin: 10px 0;
                font-weight: bold;
            }
            .connected {
                background-color: #4CAF50;
                color: white;
            }
            .disconnected {
                background-color: #f44336;
                color: white;
            }
            #messages {
                height: 400px;
                overflow-y: auto;
                border: 1px solid #ddd;
                padding: 10px;
                margin: 10px 0;
                background-color: #fafafa;
                border-radius: 5px;
            }
            .message {
                margin: 10px 0;
                padding: 10px;
                border-radius: 5px;
            }
            .user-message {
                background-color: #E3F2FD;
                text-align: right;
            }
            .bot-message {
                background-color: #F1F8E9;
            }
            .system-message {
                background-color: #FFF9C4;
                font-style: italic;
            }
            .error-message {
                background-color: #FFCDD2;
                color: #B71C1C;
            }
            .typing-message {
                background-color: #E0E0E0;
                font-style: italic;
                animation: pulse 1.5s infinite;
            }
            @keyframes pulse {
                0%, 100% { opacity: 0.6; }
                50% { opacity: 1; }
            }
            input, button {
                padding: 10px;
                margin: 5px 0;
                border: 1px solid #ddd;
                border-radius: 5px;
                font-size: 14px;
            }
            input {
                width: calc(100% - 22px);
            }
            button {
                background-color: #4CAF50;
                color: white;
                border: none;
                cursor: pointer;
                width: 100%;
                font-weight: bold;
            }
            button:hover {
                background-color: #45a049;
            }
            button:disabled {
                background-color: #cccccc;
                cursor: not-allowed;
            }
            .timestamp {
                font-size: 0.8em;
                color: #666;
                margin-left: 10px;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🏥 Medical AI Assistant - WebSocket Test</h1>
            
            <div id="status" class="status disconnected">
                ❌ Disconnected
            </div>
            
            <div>
                <input type="text" id="token" placeholder="Enter your JWT token here (from /auth/login)" />
                <button id="connect" onclick="connect()">Connect</button>
                <button id="disconnect" onclick="disconnect()" disabled>Disconnect</button>
            </div>
            
            <div id="messages"></div>
            
            <div>
                <input type="text" id="messageInput" placeholder="Type your message..." disabled />
                <button id="send" onclick="sendMessage()" disabled>Send Message</button>
            </div>
        </div>
        
        <script>
            let ws = null;
            
            function updateStatus(connected) {
                const statusEl = document.getElementById('status');
                const connectBtn = document.getElementById('connect');
                const disconnectBtn = document.getElementById('disconnect');
                const messageInput = document.getElementById('messageInput');
                const sendBtn = document.getElementById('send');
                
                if (connected) {
                    statusEl.textContent = '✅ Connected';
                    statusEl.className = 'status connected';
                    connectBtn.disabled = true;
                    disconnectBtn.disabled = false;
                    messageInput.disabled = false;
                    sendBtn.disabled = false;
                } else {
                    statusEl.textContent = '❌ Disconnected';
                    statusEl.className = 'status disconnected';
                    connectBtn.disabled = false;
                    disconnectBtn.disabled = true;
                    messageInput.disabled = true;
                    sendBtn.disabled = true;
                }
            }
            
            function addMessage(type, content, timestamp) {
                const messagesDiv = document.getElementById('messages');
                const messageDiv = document.createElement('div');
                messageDiv.className = `message ${type}-message`;
                
                const time = timestamp ? new Date(timestamp).toLocaleTimeString() : new Date().toLocaleTimeString();
                messageDiv.innerHTML = `${content}<span class="timestamp">${time}</span>`;
                
                messagesDiv.appendChild(messageDiv);
                messagesDiv.scrollTop = messagesDiv.scrollHeight;
            }
            
            function connect() {
                const token = document.getElementById('token').value.trim();
                
                if (!token) {
                    alert('Please enter your JWT token first!\\n\\nGet one by:\\n1. Go to /docs\\n2. Login via POST /auth/login\\n3. Copy the access_token');
                    return;
                }
                
                const wsUrl = `ws://localhost:8000/ws/chat?token=${token}`;
                ws = new WebSocket(wsUrl);
                
                ws.onopen = function() {
                    updateStatus(true);
                    console.log('WebSocket connected');
                };
                
                ws.onmessage = function(event) {
                    const data = JSON.parse(event.data);
                    
                    if (data.type === 'system') {
                        addMessage('system', `📢 ${data.message}`, data.timestamp);
                    } else if (data.type === 'message') {
                        addMessage('bot', `🤖 ${data.text}`, data.timestamp);
                    } else if (data.type === 'error') {
                        addMessage('error', `❌ ${data.message}`, data.timestamp);
                    } else if (data.type === 'typing') {
                        const typingDiv = document.createElement('div');
                        typingDiv.className = 'message typing-message';
                        typingDiv.id = 'typing-indicator';
                        typingDiv.textContent = data.message;
                        document.getElementById('messages').appendChild(typingDiv);
                    }
                    
                    // Remove typing indicator when response arrives
                    if (data.type === 'message') {
                        const typingIndicator = document.getElementById('typing-indicator');
                        if (typingIndicator) {
                            typingIndicator.remove();
                        }
                    }
                };
                
                ws.onerror = function(error) {
                    console.error('WebSocket error:', error);
                    addMessage('error', '❌ Connection error occurred');
                };
                
                ws.onclose = function() {
                    updateStatus(false);
                    console.log('WebSocket disconnected');
                    addMessage('system', '❌ Disconnected from server');
                };
            }
            
            function disconnect() {
                if (ws) {
                    ws.close();
                    ws = null;
                }
            }
            
            function sendMessage() {
                const input = document.getElementById('messageInput');
                const message = input.value.trim();
                
                if (!message) {
                    return;
                }
                
                if (!ws || ws.readyState !== WebSocket.OPEN) {
                    alert('Not connected! Please connect first.');
                    return;
                }
                
                // Display user message
                addMessage('user', `👤 ${message}`);
                
                // Send to server
                ws.send(JSON.stringify({
                    type: 'message',
                    text: message,
                    context: {}
                }));
                
                // Clear input
                input.value = '';
            }
            
            // Send message on Enter key
            document.getElementById('messageInput').addEventListener('keypress', function(e) {
                if (e.key === 'Enter') {
                    sendMessage();
                }
            });
            
            // Connect on Enter key in token input
            document.getElementById('token').addEventListener('keypress', function(e) {
                if (e.key === 'Enter') {
                    connect();
                }
            });
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)
