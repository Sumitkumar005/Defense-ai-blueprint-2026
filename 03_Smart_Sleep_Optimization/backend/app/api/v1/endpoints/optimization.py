"""
Sleep optimization endpoints
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime
from pydantic import BaseModel

from app.core.database import get_db
from app.services.sleep_optimizer import SleepOptimizer
from app.api.v1.endpoints.auth import get_current_user

router = APIRouter()
optimizer = SleepOptimizer()


@router.get("/optimal-sleep")
async def get_optimal_sleep(
    shift_start: datetime,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get optimal sleep timing recommendations"""
    
    # Get user's chronotype
    chronotype = current_user.chronotype.value if current_user.chronotype else "intermediate"
    
    # Calculate sleep debt (simplified)
    sleep_debt = 0.0  # Would calculate from history
    
    result = optimizer.calculate_optimal_sleep_time(
        shift_start=shift_start,
        shift_end=shift_start,  # Would get from schedule
        chronotype=chronotype,
        sleep_debt=sleep_debt
    )
    
    return result


@router.get("/nap-timing")
async def get_nap_timing(
    next_sleep: datetime,
    current_user = Depends(get_current_user)
):
    """Get optimal nap timing"""
    
    result = optimizer.calculate_nap_timing(
        current_time=datetime.utcnow(),
        next_sleep=next_sleep,
        alertness_level=0.6
    )
    
    return result or {"message": "No nap recommended at this time"}


@router.get("/caffeine-timing")
async def get_caffeine_timing(
    shift_start: datetime,
    current_user = Depends(get_current_user)
):
    """Get optimal caffeine timing"""
    
    result = optimizer.optimize_caffeine_timing(
        shift_start=shift_start,
        current_time=datetime.utcnow()
    )
    
    return result


@router.get("/alertness")
async def get_current_alertness(
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Predict current alertness level"""
    
    from app.models.sleep import SleepRecord
    from datetime import timedelta
    
    # Get recent sleep history
    cutoff = datetime.utcnow() - timedelta(days=7)
    sleep_records = db.query(SleepRecord).filter(
        SleepRecord.user_id == current_user.id,
        SleepRecord.sleep_start >= cutoff
    ).all()
    
    sleep_history = [
        {
            "duration_hours": r.duration_hours,
            "sleep_quality_score": r.sleep_quality_score
        }
        for r in sleep_records
    ]
    
    alertness = optimizer.predict_alertness(
        sleep_history=sleep_history,
        current_time=datetime.utcnow()
    )
    
    return {
        "alertness_level": alertness,
        "alertness_percentage": int(alertness * 100),
        "recommendation": "High alertness" if alertness > 0.7 else "Moderate alertness" if alertness > 0.5 else "Low alertness - rest recommended"
    }

