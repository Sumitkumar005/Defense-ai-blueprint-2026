"""
Combat Stress Resilience Training - Backend
"""

from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1 import api_router

app = FastAPI(title="Combat Stress Resilience Training")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api/v1")


@app.websocket("/ws/biometrics")
async def websocket_biometrics(websocket: WebSocket):
    """WebSocket for real-time biometric data from VR headset"""
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_json()
            # Process biometric data (HRV, skin conductance, etc.)
            # Store in database and update stress analysis
            await websocket.send_json({"status": "received"})
    except Exception as e:
        print(f"WebSocket error: {e}")


@app.get("/")
async def root():
    return {"status": "healthy", "service": "Combat Stress Resilience Training"}

