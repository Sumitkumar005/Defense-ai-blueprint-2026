from fastapi import APIRouter
from app.api.v1.endpoints import supply_chain, disruptions, suppliers

api_router = APIRouter()

api_router.include_router(supply_chain.router, prefix="/supply-chain", tags=["supply-chain"])
api_router.include_router(disruptions.router, prefix="/disruptions", tags=["disruptions"])
api_router.include_router(suppliers.router, prefix="/suppliers", tags=["suppliers"])


