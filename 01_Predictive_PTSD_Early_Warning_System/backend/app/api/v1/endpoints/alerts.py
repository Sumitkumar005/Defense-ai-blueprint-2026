"""
Alert endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

from app.core.database import get_db
from app.models.user import User, UserRole
from app.models.alert import Alert, AlertStatus, AlertSeverity
from app.api.v1.endpoints.auth import get_current_user

router = APIRouter()


class AlertResponse(BaseModel):
    """Alert response model"""
    id: int
    user_id: int
    severity: str
    status: str
    title: str
    message: str
    intervention_recommendations: Optional[str]
    created_at: datetime
    acknowledged_at: Optional[datetime]
    resolved_at: Optional[datetime]
    is_active: bool
    
    class Config:
        from_attributes = True


class AlertUpdate(BaseModel):
    """Alert update model"""
    status: Optional[AlertStatus] = None


@router.get("/", response_model=List[AlertResponse])
async def get_alerts(
    severity: Optional[AlertSeverity] = None,
    status: Optional[AlertStatus] = None,
    active_only: bool = True,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get alerts for current user or unit (if commander)"""
    query = db.query(Alert)
    
    # Commanders can see unit alerts, soldiers see only their own
    if current_user.role == UserRole.COMMANDER:
        from app.models.user import User
        unit_users = db.query(User.id).filter(User.unit_id == current_user.unit_id).subquery()
        query = query.filter(Alert.user_id.in_(unit_users))
    else:
        query = query.filter(Alert.user_id == current_user.id)
    
    if severity:
        query = query.filter(Alert.severity == severity)
    
    if status:
        query = query.filter(Alert.status == status)
    
    if active_only:
        query = query.filter(Alert.is_active == True)
    
    query = query.order_by(desc(Alert.created_at))
    
    alerts = query.all()
    return alerts


@router.patch("/{alert_id}", response_model=AlertResponse)
async def update_alert(
    alert_id: int,
    alert_update: AlertUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update alert status"""
    alert = db.query(Alert).filter(Alert.id == alert_id).first()
    
    if not alert:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Alert not found"
        )
    
    # Check permissions
    if alert.user_id != current_user.id and current_user.role not in [UserRole.COMMANDER, UserRole.MENTAL_HEALTH_COORDINATOR]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this alert"
        )
    
    if alert_update.status:
        alert.status = alert_update.status
        if alert_update.status == AlertStatus.ACKNOWLEDGED:
            alert.acknowledged_at = datetime.utcnow()
            alert.acknowledged_by = current_user.id
        elif alert_update.status == AlertStatus.RESOLVED:
            alert.resolved_at = datetime.utcnow()
            alert.is_active = False
    
    db.commit()
    db.refresh(alert)
    
    return alert

