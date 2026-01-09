"""
Predictive Maintenance for Military Vehicles - Main Application
"""

from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.v1 import api_router

app = FastAPI(
    title="Predictive Maintenance for Military Vehicles",
    description="IoT + ML system for vehicle maintenance prediction",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api/v1")


@app.websocket("/ws/telematics")
async def websocket_telematics(websocket: WebSocket):
    """WebSocket for real-time vehicle telematics data"""
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_json()
            # Process telematics data
            # Store in TimescaleDB
            # Trigger ML prediction if needed
            await websocket.send_json({"status": "received"})
    except Exception as e:
        print(f"WebSocket error: {e}")


@app.get("/")
async def root():
    return {"status": "healthy", "service": "Predictive Maintenance System"}

