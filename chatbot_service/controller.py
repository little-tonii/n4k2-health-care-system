from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import List
import json
import numpy as np
from .ai import model, diseases, predict_with_uncertainty

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
                # Convert symptoms to input array
                input_symptoms = [1 if symptom in data["symptoms"] else 0 for symptom in [
                    "Fever", "Cough", "Sore throat", "Fatigue", "Shortness of breath",
                    "Chest pain", "Headache", "Runny nose", "Sneezing", "Muscle pain",
                    "Joint pain", "Nausea", "Vomiting", "Diarrhea", "Abdominal pain",
                    "Weight loss", "Irritability", "Rash", "Swelling", "Anxiety",
                    "Depressed mood", "Itching", "Dizziness", "Palpitations", "Blurred vision"
                ]]
                
                input_array = np.array([input_symptoms], dtype=np.float32)
                mean_probs, std_probs = predict_with_uncertainty(model, input_array)
                
                # Get top 3 diagnoses
                top_indices = np.argsort(mean_probs[0])[-3:][::-1]
                diagnoses = []
                
                for idx in top_indices:
                    diagnosis = {
                        "disease": diseases[idx],
                        "probability": float(mean_probs[0][idx]),
                        "uncertainty": float(std_probs[0][idx])
                    }
                    diagnoses.append(diagnosis)
                
                # Load treatment data
                with open('./chatbot_service/data.json', 'r') as f:
                    treatment_data = json.load(f)
                
                # Add treatment information
                for diagnosis in diagnoses:
                    disease = diagnosis["disease"]
                    if disease in treatment_data:
                        diagnosis.update(treatment_data[disease])
                
                await manager.send_message(json.dumps({
                    "type": "diagnosis",
                    "diagnoses": diagnoses
                }), websocket)
            
    except WebSocketDisconnect:
        manager.disconnect(websocket) 