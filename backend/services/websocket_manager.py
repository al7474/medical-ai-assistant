"""
WebSocket Connection Manager
Manages active WebSocket connections for real-time chat
"""
from typing import Dict, List
from fastapi import WebSocket, WebSocketDisconnect
import json
from datetime import datetime


class ConnectionManager:
    """
    Manages WebSocket connections for real-time chat
    Supports multiple concurrent users
    """
    
    def __init__(self):
        # Store active connections: {user_id: [websockets]}
        self.active_connections: Dict[int, List[WebSocket]] = {}
        # Store connection metadata
        self.connection_info: Dict[WebSocket, dict] = {}
    
    async def connect(self, websocket: WebSocket, user_id: int, user_name: str):
        """
        Accept and register a new WebSocket connection
        
        Args:
            websocket: WebSocket connection
            user_id: User's database ID
            user_name: User's name for display
        """
        await websocket.accept()
        
        # Add to active connections
        if user_id not in self.active_connections:
            self.active_connections[user_id] = []
        
        self.active_connections[user_id].append(websocket)
        
        # Store metadata
        self.connection_info[websocket] = {
            "user_id": user_id,
            "user_name": user_name,
            "connected_at": datetime.utcnow()
        }
        
        print(f"✅ WebSocket connected: {user_name} (ID: {user_id})")
        print(f"📊 Total active connections: {self.get_total_connections()}")
    
    def disconnect(self, websocket: WebSocket):
        """
        Remove a WebSocket connection
        
        Args:
            websocket: WebSocket to disconnect
        """
        if websocket in self.connection_info:
            info = self.connection_info[websocket]
            user_id = info["user_id"]
            user_name = info["user_name"]
            
            # Remove from active connections
            if user_id in self.active_connections:
                if websocket in self.active_connections[user_id]:
                    self.active_connections[user_id].remove(websocket)
                
                # Clean up empty user entries
                if not self.active_connections[user_id]:
                    del self.active_connections[user_id]
            
            # Remove metadata
            del self.connection_info[websocket]
            
            print(f"❌ WebSocket disconnected: {user_name} (ID: {user_id})")
            print(f"📊 Total active connections: {self.get_total_connections()}")
    
    async def send_personal_message(self, message: dict, websocket: WebSocket):
        """
        Send a message to a specific connection
        
        Args:
            message: Message dictionary to send
            websocket: Target WebSocket connection
        """
        try:
            await websocket.send_json(message)
        except Exception as e:
            print(f"❌ Error sending message: {e}")
    
    async def send_to_user(self, message: dict, user_id: int):
        """
        Send a message to all connections of a specific user
        
        Args:
            message: Message dictionary to send
            user_id: Target user ID
        """
        if user_id in self.active_connections:
            for connection in self.active_connections[user_id]:
                await self.send_personal_message(message, connection)
    
    async def broadcast(self, message: dict):
        """
        Send a message to all connected users
        
        Args:
            message: Message dictionary to broadcast
        """
        for user_connections in self.active_connections.values():
            for connection in user_connections:
                await self.send_personal_message(message, connection)
    
    def get_total_connections(self) -> int:
        """Get total number of active connections"""
        return sum(len(conns) for conns in self.active_connections.values())
    
    def get_active_users(self) -> List[dict]:
        """Get list of active users"""
        users = []
        seen_user_ids = set()
        
        for websocket, info in self.connection_info.items():
            user_id = info["user_id"]
            if user_id not in seen_user_ids:
                users.append({
                    "user_id": user_id,
                    "user_name": info["user_name"],
                    "connections": len(self.active_connections.get(user_id, [])),
                    "connected_at": info["connected_at"].isoformat()
                })
                seen_user_ids.add(user_id)
        
        return users


# Global connection manager instance
manager = ConnectionManager()


def get_connection_manager() -> ConnectionManager:
    """Get the global connection manager instance"""
    return manager
