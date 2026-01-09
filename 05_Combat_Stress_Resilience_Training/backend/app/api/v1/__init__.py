from fastapi import APIRouter
from app.api.v1.endpoints import training, sessions

api_router = APIRouter()

api_router.include_router(training.router, prefix="/training", tags=["training"])
api_router.include_router(sessions.router, prefix="/sessions", tags=["sessions"])

