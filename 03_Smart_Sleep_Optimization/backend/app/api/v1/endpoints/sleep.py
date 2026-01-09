"""
Sleep tracking endpoints
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List
from pydantic import BaseModel

from app.core.database import get_db
from app.models.sleep import SleepRecord
from app.api.v1.endpoints.auth import get_current_user

router = APIRouter()


class SleepRecordCreate(BaseModel):
    sleep_start: datetime
    sleep_end: datetime
    duration_hours: float
    deep_sleep_minutes: float = None
    rem_sleep_minutes: float = None
    light_sleep_minutes: float = None
    sleep_quality_score: float = None
    source: str = "manual"


class SleepRecordResponse(BaseModel):
    id: int
    user_id: int
    sleep_start: datetime
    sleep_end: datetime
    duration_hours: float
    sleep_quality_score: float = None
    
    class Config:
        from_attributes = True


@router.post("/", response_model=SleepRecordResponse)
async def create_sleep_record(
    record: SleepRecordCreate,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create sleep record"""
    sleep_record = SleepRecord(
        user_id=current_user.id,
        **record.dict()
    )
    db.add(sleep_record)
    db.commit()
    db.refresh(sleep_record)
    return sleep_record


@router.get("/", response_model=List[SleepRecordResponse])
async def get_sleep_records(
    days: int = 30,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get sleep records"""
    from datetime import timedelta
    cutoff = datetime.utcnow() - timedelta(days=days)
    
    records = db.query(SleepRecord).filter(
        SleepRecord.user_id == current_user.id,
        SleepRecord.sleep_start >= cutoff
    ).order_by(SleepRecord.sleep_start.desc()).all()
    
    return records

