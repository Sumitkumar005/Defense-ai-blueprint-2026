"""
Analytics endpoints for unit-level insights
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func, case
from typing import Dict, List
from pydantic import BaseModel

from app.core.database import get_db
from app.models.user import User, UserRole
from app.models.prediction import PTSDPrediction, RiskLevel
from app.models.alert import Alert, AlertSeverity
from app.api.v1.endpoints.auth import get_current_user

router = APIRouter()


class UnitAnalyticsResponse(BaseModel):
    """Unit analytics response model"""
    unit_id: int
    total_soldiers: int
    risk_distribution: Dict[str, int]
    active_alerts: Dict[str, int]
    trend_data: List[Dict]
    average_risk_score: float


@router.get("/unit", response_model=UnitAnalyticsResponse)
async def get_unit_analytics(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get unit-level analytics (commander only)"""
    if current_user.role != UserRole.COMMANDER:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only commanders can access unit analytics"
        )
    
    if not current_user.unit_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User is not assigned to a unit"
        )
    
    # Get unit soldiers
    unit_soldiers = db.query(User.id).filter(
        User.unit_id == current_user.unit_id,
        User.role == UserRole.SOLDIER
    ).subquery()
    
    # Get latest predictions for unit
    latest_predictions = db.query(PTSDPrediction).filter(
        PTSDPrediction.user_id.in_(unit_soldiers)
    ).order_by(PTSDPrediction.prediction_date.desc()).distinct(PTSDPrediction.user_id).all()
    
    # Calculate risk distribution
    risk_distribution = {
        "green": 0,
        "yellow": 0,
        "red": 0
    }
    
    total_risk_score = 0.0
    for pred in latest_predictions:
        risk_distribution[pred.risk_level.value] = risk_distribution.get(pred.risk_level.value, 0) + 1
        total_risk_score += pred.risk_score
    
    average_risk_score = total_risk_score / len(latest_predictions) if latest_predictions else 0.0
    
    # Get active alerts
    active_alerts = db.query(
        Alert.severity,
        func.count(Alert.id).label("count")
    ).filter(
        Alert.user_id.in_(unit_soldiers),
        Alert.is_active == True
    ).group_by(Alert.severity).all()
    
    alert_counts = {
        "green": 0,
        "yellow": 0,
        "red": 0
    }
    for severity, count in active_alerts:
        alert_counts[severity.value] = count
    
    # Get trend data (simplified - would need time-series aggregation in production)
    trend_data = []
    
    return UnitAnalyticsResponse(
        unit_id=current_user.unit_id,
        total_soldiers=len(unit_soldiers),
        risk_distribution=risk_distribution,
        active_alerts=alert_counts,
        trend_data=trend_data,
        average_risk_score=average_risk_score
    )

