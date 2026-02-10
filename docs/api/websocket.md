# 🌐 WebSocket Real-Time Chat

Complete guide to using WebSocket for real-time bidirectional communication with the AI Medical Assistant.

## 📚 Table of Contents

- [Overview](#overview)
- [Authentication](#authentication)
- [Endpoints](#endpoints)
- [Message Format](#message-format)
- [Usage Examples](#usage-examples)
- [Connection Manager](#connection-manager)
- [Error Handling](#error-handling)
- [Best Practices](#best-practices)
- [Testing](#testing)

## 🔍 Overview

The WebSocket integration enables:
- ✅ **Real-time bidirectional communication** between clients and AI
- ✅ **JWT-based authentication** for secure connections
- ✅ **Multiple concurrent users** with connection tracking
- ✅ **Typing indicators** for better UX
- ✅ **System messages** for connection events
- ✅ **AI integration** with fallback mode

## 🔐 Authentication

WebSocket connections require a valid JWT token. The token must be passed as a query parameter.

### Getting a Token

First, obtain a token using the authentication endpoints:

```bash
# Login to get token
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=user@example.com&password=YourPassword123!"

# Response:
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### Connection URL

Use the token to connect to WebSocket:

```
ws://localhost:8000/ws/chat?token=YOUR_JWT_TOKEN
```

## 📡 Endpoints

### WebSocket Chat Endpoint

**Endpoint:** `WebSocket /ws/chat`

**Query Parameters:**
- `token` (required): JWT authentication token

**Connection Flow:**
1. Client connects with valid JWT token
2. Server validates token and authenticates user
3. Server sends welcome message
4. Bidirectional communication begins

### Active Users Endpoint

**Endpoint:** `GET /ws/active-users`

Returns information about currently connected users.

**Response:**
```json
{
  "active_users": [
    {
      "user_id": 1,
      "user_name": "John Doe",
      "user_email": "john@example.com",
      "connections": 2,
      "connection_ids": ["conn_123", "conn_456"]
    }
  ],
  "total_connections": 2
}
```

### Test Client

**Endpoint:** `GET /ws/test-client`

Returns an HTML page with an interactive WebSocket test client.

## 📨 Message Format

### Client → Server (Outgoing)

```json
{
  "type": "message",
  "text": "What should I do if I have a headache?",
  "context": {
    "additional": "data"
  }
}
```

**Fields:**
- `type`: Message type (currently only "message" supported)
- `text`: The message content
- `context`: Optional additional context

### Server → Client (Incoming)

#### Regular Message

```json
{
  "type": "message",
  "text": "For headaches, I recommend...",
  "provider": "openai",
  "model": "gpt-4",
  "timestamp": "2024-02-10T12:30:45.123456"
}
```

#### System Message

```json
{
  "type": "system",
  "message": "Welcome John! Connected to AI Medical Assistant",
  "timestamp": "2024-02-10T12:30:40.123456"
}
```

#### Typing Indicator

```json
{
  "type": "typing",
  "message": "AI is thinking...",
  "timestamp": "2024-02-10T12:30:41.123456"
}
```

#### Error Message

```json
{
  "type": "error",
  "message": "Failed to process your request",
  "timestamp": "2024-02-10T12:30:42.123456"
}
```

## 💻 Usage Examples

### Python Client

```python
import asyncio
import websockets
import json

async def chat():
    token = "YOUR_JWT_TOKEN"
    uri = f"ws://localhost:8000/ws/chat?token={token}"
    
    async with websockets.connect(uri) as websocket:
        # Receive welcome message
        welcome = await websocket.recv()
        print(f"Server: {json.loads(welcome)}")
        
        # Send message
        message = {
            "type": "message",
            "text": "Hello, I need medical advice"
        }
        await websocket.send(json.dumps(message))
        
        # Receive typing indicator
        typing = await websocket.recv()
        print(f"Typing: {json.loads(typing)}")
        
        # Receive response
        response = await websocket.recv()
        data = json.loads(response)
        print(f"AI: {data['text']}")

asyncio.run(chat())
```

### JavaScript Client (Browser)

```javascript
// Get token from login
const response = await fetch('http://localhost:8000/auth/login', {
  method: 'POST',
  headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
  body: 'username=user@example.com&password=pass123'
});
const { access_token } = await response.json();

// Connect to WebSocket
const ws = new WebSocket(`ws://localhost:8000/ws/chat?token=${access_token}`);

ws.onopen = () => {
  console.log('Connected!');
  
  // Send message
  ws.send(JSON.stringify({
    type: 'message',
    text: 'Hello! Can you help me?'
  }));
};

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  
  switch(data.type) {
    case 'system':
      console.log(`System: ${data.message}`);
      break;
    case 'typing':
      console.log('AI is typing...');
      break;
    case 'message':
      console.log(`AI: ${data.text}`);
      console.log(`Provider: ${data.provider}, Model: ${data.model}`);
      break;
    case 'error':
      console.error(`Error: ${data.message}`);
      break;
  }
};

ws.onerror = (error) => {
  console.error('WebSocket error:', error);
};

ws.onclose = () => {
  console.log('Disconnected');
};
```

### JavaScript with React

```javascript
import { useEffect, useState, useRef } from 'react';

function ChatComponent({ token }) {
  const [messages, setMessages] = useState([]);
  const [isTyping, setIsTyping] = useState(false);
  const ws = useRef(null);
  
  useEffect(() => {
    // Connect
    ws.current = new WebSocket(`ws://localhost:8000/ws/chat?token=${token}`);
    
    ws.current.onmessage = (event) => {
      const data = JSON.parse(event.data);
      
      if (data.type === 'message') {
        setMessages(prev => [...prev, { role: 'assistant', text: data.text }]);
        setIsTyping(false);
      } else if (data.type === 'typing') {
        setIsTyping(true);
      } else if (data.type === 'system') {
        console.log('System:', data.message);
      }
    };
    
    // Cleanup
    return () => ws.current?.close();
  }, [token]);
  
  const sendMessage = (text) => {
    setMessages(prev => [...prev, { role: 'user', text }]);
    ws.current.send(JSON.stringify({ type: 'message', text }));
  };
  
  return (
    <div>
      {messages.map((msg, i) => (
        <div key={i} className={msg.role}>
          {msg.text}
        </div>
      ))}
      {isTyping && <div>AI is typing...</div>}
      <input onKeyPress={e => {
        if (e.key === 'Enter') {
          sendMessage(e.target.value);
          e.target.value = '';
        }
      }} />
    </div>
  );
}
```

## 🔧 Connection Manager

The `ConnectionManager` class handles all active WebSocket connections:

```python
from services.websocket_manager import manager

# Connect a user
await manager.connect(websocket, user_id, user_name, user_email)

# Send to specific user
await manager.send_personal_message({"text": "Hello!"}, user_id)

# Broadcast to all users
await manager.broadcast({"text": "System maintenance in 5 min"})

# Get active users
active = manager.get_active_users()

# Disconnect user
manager.disconnect(user_id, connection_id)
```

### Features

- **Multiple connections per user**: Same user can connect from different devices
- **Connection metadata**: Track user details for each connection
- **Broadcast capability**: Send messages to all connected users
- **Personal messaging**: Send to specific users only
- **Active user tracking**: Get list of currently connected users

## ⚠️ Error Handling

### Common Errors

#### 401 Unauthorized

**Cause:** Invalid or expired JWT token

**Solution:**
```python
# Get a new token
response = requests.post("http://localhost:8000/auth/login", 
                         data={"username": "user@example.com", "password": "pass"})
token = response.json()["access_token"]
```

#### 403 Forbidden

**Cause:** User account is not active

**Solution:** Contact administrator to activate account

#### Connection Closed Unexpectedly

**Cause:** Network issues or server restart

**Solution:** Implement reconnection logic:

```javascript
function connectWithRetry(token, maxRetries = 5) {
  let retries = 0;
  
  function connect() {
    const ws = new WebSocket(`ws://localhost:8000/ws/chat?token=${token}`);
    
    ws.onclose = () => {
      if (retries < maxRetries) {
        retries++;
        console.log(`Reconnecting... (${retries}/${maxRetries})`);
        setTimeout(connect, 1000 * retries); // Exponential backoff
      }
    };
    
    return ws;
  }
  
  return connect();
}
```

## ✨ Best Practices

### 1. Token Management

```javascript
// Refresh token before expiration
async function refreshTokenIfNeeded() {
  const tokenExpiry = localStorage.getItem('token_expiry');
  const now = Date.now();
  
  // Refresh 5 minutes before expiration
  if (now > tokenExpiry - (5 * 60 * 1000)) {
    const newToken = await refreshToken();
    reconnectWebSocket(newToken);
  }
}
```

### 2. Message Queuing

```javascript
class WSManager {
  constructor(token) {
    this.messageQueue = [];
    this.connected = false;
    this.connect(token);
  }
  
  connect(token) {
    this.ws = new WebSocket(`ws://localhost:8000/ws/chat?token=${token}`);
    
    this.ws.onopen = () => {
      this.connected = true;
      // Send queued messages
      while (this.messageQueue.length > 0) {
        this.ws.send(this.messageQueue.shift());
      }
    };
  }
  
  send(data) {
    const message = JSON.stringify(data);
    
    if (this.connected) {
      this.ws.send(message);
    } else {
      this.messageQueue.push(message);
    }
  }
}
```

### 3. Heartbeat/Ping

```javascript
// Keep connection alive
function startHeartbeat(ws) {
  const interval = setInterval(() => {
    if (ws.readyState === WebSocket.OPEN) {
      ws.send(JSON.stringify({ type: 'ping' }));
    } else {
      clearInterval(interval);
    }
  }, 30000); // Every 30 seconds
}
```

### 4. Memory Management

```javascript
// Cleanup on unmount (React)
useEffect(() => {
  const ws = new WebSocket(url);
  
  return () => {
    ws.close();
    // Clear any message listeners
  };
}, []);
```

## 🧪 Testing

### Automated Testing

Run the test script:

```bash
cd backend
python test_websocket.py
```

**Tests:**
- ✅ User registration and login
- ✅ WebSocket connection with JWT
- ✅ Sending messages
- ✅ Receiving AI responses
- ✅ Typing indicators
- ✅ System messages
- ✅ Active users endpoint

### Manual Testing

1. **Start the server:**
   ```bash
   cd backend
   uvicorn main:app --reload
   ```

2. **Open test client:**
   ```
   http://localhost:8000/ws/test-client
   ```

3. **Get a token:**
   - Use `/auth/login` endpoint
   - Or use the test credentials from `test_websocket.py`

4. **Connect:**
   - Paste token in test client
   - Click "Connect"
   - Send messages

### Load Testing

```python
import asyncio
import websockets

async def simulate_user(user_id, token):
    uri = f"ws://localhost:8000/ws/chat?token={token}"
    async with websockets.connect(uri) as ws:
        await ws.recv()  # Welcome
        await ws.send('{"type": "message", "text": "Hello"}')
        await ws.recv()  # Response
        await asyncio.sleep(10)  # Stay connected

async def load_test(num_users=10):
    tokens = [get_token_for_user(i) for i in range(num_users)]
    tasks = [simulate_user(i, token) for i, token in enumerate(tokens)]
    await asyncio.gather(*tasks)

asyncio.run(load_test(50))  # 50 concurrent users
```

## 🔒 Security Considerations

1. **Token Security**
   - Never expose tokens in URLs (use only in WebSocket upgrade)
   - Implement token rotation
   - Use short expiration times for sensitive operations

2. **Rate Limiting**
   - Limit messages per user per minute
   - Prevent spam and abuse
   - Monitor connection attempts

3. **Input Validation**
   - Validate all incoming messages
   - Sanitize user input
   - Check message size limits

4. **Connection Limits**
   - Limit connections per user
   - Maximum concurrent connections
   - Timeout idle connections

## 📊 Monitoring

Track these metrics:

- Active connections count
- Messages per second
- Average response time
- Connection duration
- Error rates
- Token validation failures

## 🚀 Production Deployment

For production, consider:

1. **Use WSS (WebSocket Secure)**
   ```python
   wss://api.yourapp.com/ws/chat?token=...
   ```

2. **Load Balancing**
   - Use sticky sessions or shared state
   - Redis for cross-server communication

3. **Monitoring**
   - Track connection health
   - Log errors and metrics
   - Alert on anomalies

4. **Scaling**
   - Horizontal scaling with Redis pub/sub
   - Connection pooling
   - Message queuing

## 📝 API Summary

| Endpoint | Type | Auth | Description |
|----------|------|------|-------------|
| `/ws/chat?token=xxx` | WebSocket | JWT | Real-time chat |
| `/ws/active-users` | GET | None | List active users |
| `/ws/test-client` | GET | None | HTML test client |

## 🆘 Support

For issues or questions:
1. Check server logs: `tail -f logs/app.log`
2. Test with HTML client: `/ws/test-client`
3. Verify token validity: `/auth/me`
4. Check active users: `/ws/active-users`

---

**Version:** 0.3.0  
**Last Updated:** 2024-02-10  
**Status:** ✅ Production Ready
