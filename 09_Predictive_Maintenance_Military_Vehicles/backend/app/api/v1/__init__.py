from fastapi import APIRouter
from app.api.v1.endpoints import vehicles, predictions, maintenance

api_router = APIRouter()

api_router.include_router(vehicles.router, prefix="/vehicles", tags=["vehicles"])
api_router.include_router(predictions.router, prefix="/predictions", tags=["predictions"])
api_router.include_router(maintenance.router, prefix="/maintenance", tags=["maintenance"])


