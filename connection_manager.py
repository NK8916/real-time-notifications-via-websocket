from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from typing import List

class ConnectionManager:
    def __init__(self):
        self.connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.connections.append(websocket)
    
    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self,websocket:WebSocket,data: str):
        for connection in self.connections:
            if connection!=websocket:
                await connection.send_text(data)
    def disconnect(self):
        for connection in self.connections:
            self.connections.remove(connection)
