"""
Shift schedule endpoints
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List
from pydantic import BaseModel

from app.core.database import get_db
from app.models.sleep import ShiftSchedule
from app.api.v1.endpoints.auth import get_current_user

router = APIRouter()


class ShiftScheduleCreate(BaseModel):
    shift_start: datetime
    shift_end: datetime
    shift_type: str = None


@router.post("/")
async def create_shift_schedule(
    schedule: ShiftScheduleCreate,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create shift schedule"""
    shift = ShiftSchedule(
        user_id=current_user.id,
        **schedule.dict()
    )
    db.add(shift)
    db.commit()
    db.refresh(shift)
    return shift


@router.get("/")
async def get_shift_schedules(
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user's shift schedules"""
    shifts = db.query(ShiftSchedule).filter(
        ShiftSchedule.user_id == current_user.id
    ).order_by(ShiftSchedule.shift_start.desc()).limit(30).all()
    
    return shifts

