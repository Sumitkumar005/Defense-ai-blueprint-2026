from fastapi import APIRouter
from app.api.v1.endpoints import sleep, shifts, optimization

api_router = APIRouter()

api_router.include_router(sleep.router, prefix="/sleep", tags=["sleep"])
api_router.include_router(shifts.router, prefix="/shifts", tags=["shifts"])
api_router.include_router(optimization.router, prefix="/optimization", tags=["optimization"])

