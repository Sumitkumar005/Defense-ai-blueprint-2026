from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.supply_chain import Supplier

router = APIRouter()


@router.get("/")
async def get_suppliers(db: Session = Depends(get_db)):
    """Get all suppliers"""
    suppliers = db.query(Supplier).all()
    return {"suppliers": suppliers}


@router.get("/{supplier_id}/performance")
async def get_supplier_performance(supplier_id: int, db: Session = Depends(get_db)):
    """Get supplier performance metrics"""
    supplier = db.query(Supplier).filter(Supplier.id == supplier_id).first()
    if not supplier:
        return {"error": "Supplier not found"}
    
    return {
        "supplier_id": supplier_id,
        "reliability_score": supplier.reliability_score,
        "quality_score": supplier.quality_score,
        "delivery_performance": supplier.delivery_performance,
        "risk_factors": supplier.risk_factors
    }


