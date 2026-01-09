"""
Health metrics endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import List, Optional
from datetime import datetime, timedelta
from pydantic import BaseModel

from app.core.database import get_db
from app.models.user import User
from app.models.health_metric import HealthMetric, MetricType
from app.api.v1.endpoints.auth import get_current_user

router = APIRouter()


class HealthMetricCreate(BaseModel):
    """Health metric creation model"""
    metric_type: MetricType
    value: Optional[float] = None
    metadata: Optional[dict] = None
    recorded_at: Optional[datetime] = None
    source: Optional[str] = None


class HealthMetricResponse(BaseModel):
    """Health metric response model"""
    id: int
    user_id: int
    metric_type: str
    value: Optional[float]
    metadata: Optional[dict]
    recorded_at: datetime
    source: Optional[str]
    
    class Config:
        from_attributes = True


@router.post("/", response_model=HealthMetricResponse)
async def create_metric(
    metric_data: HealthMetricCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new health metric"""
    new_metric = HealthMetric(
        user_id=current_user.id,
        metric_type=metric_data.metric_type,
        value=metric_data.value,
        metadata=metric_data.metadata,
        recorded_at=metric_data.recorded_at or datetime.utcnow(),
        source=metric_data.source
    )
    
    db.add(new_metric)
    db.commit()
    db.refresh(new_metric)
    
    return new_metric


@router.get("/", response_model=List[HealthMetricResponse])
async def get_metrics(
    metric_type: Optional[MetricType] = None,
    days: int = 30,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get health metrics for current user"""
    query = db.query(HealthMetric).filter(HealthMetric.user_id == current_user.id)
    
    if metric_type:
        query = query.filter(HealthMetric.metric_type == metric_type)
    
    cutoff_date = datetime.utcnow() - timedelta(days=days)
    query = query.filter(HealthMetric.recorded_at >= cutoff_date)
    query = query.order_by(desc(HealthMetric.recorded_at))
    
    metrics = query.all()
    return metrics


@router.post("/batch", response_model=List[HealthMetricResponse])
async def create_metrics_batch(
    metrics_data: List[HealthMetricCreate],
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create multiple health metrics at once (for data ingestion)"""
    new_metrics = []
    for metric_data in metrics_data:
        metric = HealthMetric(
            user_id=current_user.id,
            metric_type=metric_data.metric_type,
            value=metric_data.value,
            metadata=metric_data.metadata,
            recorded_at=metric_data.recorded_at or datetime.utcnow(),
            source=metric_data.source
        )
        new_metrics.append(metric)
        db.add(metric)
    
    db.commit()
    for metric in new_metrics:
        db.refresh(metric)
    
    return new_metrics

