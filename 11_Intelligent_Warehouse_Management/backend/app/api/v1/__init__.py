from fastapi import APIRouter
from app.api.v1.endpoints import inventory, picking, quality

api_router = APIRouter()

api_router.include_router(inventory.router, prefix="/inventory", tags=["inventory"])
api_router.include_router(picking.router, prefix="/picking", tags=["picking"])
api_router.include_router(quality.router, prefix="/quality", tags=["quality"])


