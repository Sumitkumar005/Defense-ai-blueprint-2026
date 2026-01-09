"""
API v1 router
"""

from fastapi import APIRouter
from app.api.v1.endpoints import auth, users, metrics, predictions, alerts, analytics

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(metrics.router, prefix="/metrics", tags=["health-metrics"])
api_router.include_router(predictions.router, prefix="/predictions", tags=["predictions"])
api_router.include_router(alerts.router, prefix="/alerts", tags=["alerts"])
api_router.include_router(analytics.router, prefix="/analytics", tags=["analytics"])

