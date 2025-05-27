from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import List
import json
from .ai import get_diagnosis, SYMPTOMS

router = APIRouter(prefix="/chatbot", tags=["Chatbot"])

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

manager = ConnectionManager()

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            data = json.loads(data)
            
            if data["type"] == "symptoms":
                # Get diagnosis using the new AI module
                diagnoses = get_diagnosis(data["symptoms"])
                
                # Send diagnosis back to client
                await manager.send_message(json.dumps({
                    "type": "diagnosis",
                    "diagnoses": diagnoses
                }), websocket)
            
    except WebSocketDisconnect:
        manager.disconnect(websocket) 