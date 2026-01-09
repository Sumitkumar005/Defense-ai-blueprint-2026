from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.vehicle import Vehicle

router = APIRouter()


@router.get("/")
async def get_vehicles(db: Session = Depends(get_db)):
    """Get all vehicles"""
    vehicles = db.query(Vehicle).all()
    return {"vehicles": vehicles}


@router.get("/{vehicle_id}")
async def get_vehicle(vehicle_id: str, db: Session = Depends(get_db)):
    """Get vehicle details"""
    vehicle = db.query(Vehicle).filter(Vehicle.vehicle_id == vehicle_id).first()
    if not vehicle:
        return {"error": "Vehicle not found"}
    return vehicle


@router.get("/{vehicle_id}/telematics")
async def get_telematics(
    vehicle_id: str,
    hours: int = 24,
    db: Session = Depends(get_db)
):
    """Get recent telematics data"""
    from app.core.database import get_timescale_db
    from app.models.vehicle import TelematicsData
    from datetime import datetime, timedelta
    
    timescale_db = next(get_timescale_db())
    
    cutoff = datetime.utcnow() - timedelta(hours=hours)
    data = timescale_db.query(TelematicsData).filter(
        TelematicsData.vehicle_id == vehicle_id,
        TelematicsData.timestamp >= cutoff
    ).order_by(TelematicsData.timestamp.desc()).limit(1000).all()
    
    return {"telematics": data}


