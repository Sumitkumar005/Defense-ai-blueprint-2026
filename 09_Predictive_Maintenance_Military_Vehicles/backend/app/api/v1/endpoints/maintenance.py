from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.vehicle import MaintenanceRecord, Vehicle
from pydantic import BaseModel
from datetime import datetime

router = APIRouter()


class MaintenanceRecordCreate(BaseModel):
    vehicle_id: str
    maintenance_type: str
    component: str
    description: str
    cost: float = 0.0
    duration_hours: float = 0.0
    mechanic_notes: str = ""


@router.post("/")
async def create_maintenance_record(
    record: MaintenanceRecordCreate,
    db: Session = Depends(get_db)
):
    """Create maintenance record"""
    vehicle = db.query(Vehicle).filter(Vehicle.vehicle_id == record.vehicle_id).first()
    if not vehicle:
        return {"error": "Vehicle not found"}
    
    maintenance = MaintenanceRecord(
        vehicle_id=vehicle.id,
        maintenance_type=record.maintenance_type,
        component=record.component,
        description=record.description,
        cost=record.cost,
        duration_hours=record.duration_hours,
        mechanic_notes=record.mechanic_notes
    )
    
    db.add(maintenance)
    db.commit()
    db.refresh(maintenance)
    
    return maintenance


@router.get("/{vehicle_id}")
async def get_maintenance_history(
    vehicle_id: str,
    db: Session = Depends(get_db)
):
    """Get maintenance history for vehicle"""
    vehicle = db.query(Vehicle).filter(Vehicle.vehicle_id == vehicle_id).first()
    if not vehicle:
        return {"error": "Vehicle not found"}
    
    records = db.query(MaintenanceRecord).filter(
        MaintenanceRecord.vehicle_id == vehicle.id
    ).order_by(MaintenanceRecord.performed_at.desc()).limit(50).all()
    
    return {"maintenance_records": records}


