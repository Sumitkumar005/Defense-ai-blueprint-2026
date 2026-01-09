"""
PTSD prediction endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

from app.core.database import get_db
from app.models.user import User
from app.models.prediction import PTSDPrediction, RiskLevel, PredictionTimeframe
from app.api.v1.endpoints.auth import get_current_user
from app.services.ml_service import MLPredictionService

router = APIRouter()


class PredictionResponse(BaseModel):
    """Prediction response model"""
    id: int
    user_id: int
    risk_level: str
    risk_score: float
    timeframe: str
    prediction_date: datetime
    model_version: Optional[str]
    feature_contributions: Optional[dict]
    confidence_score: Optional[float]
    
    class Config:
        from_attributes = True


@router.post("/generate", response_model=PredictionResponse)
async def generate_prediction(
    timeframe: PredictionTimeframe = PredictionTimeframe.THIRTY_DAYS,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Generate new PTSD risk prediction for user"""
    ml_service = MLPredictionService()
    
    # Get user's recent health metrics
    from app.models.health_metric import HealthMetric
    from datetime import timedelta
    
    cutoff_date = datetime.utcnow() - timedelta(days=90)
    metrics = db.query(HealthMetric).filter(
        HealthMetric.user_id == current_user.id,
        HealthMetric.recorded_at >= cutoff_date
    ).all()
    
    # Generate prediction using ML service
    prediction_result = await ml_service.predict_ptsd_risk(
        user_id=current_user.id,
        metrics=metrics,
        timeframe=timeframe
    )
    
    # Save prediction to database
    new_prediction = PTSDPrediction(
        user_id=current_user.id,
        risk_level=prediction_result["risk_level"],
        risk_score=prediction_result["risk_score"],
        timeframe=timeframe,
        model_version=prediction_result.get("model_version"),
        feature_contributions=prediction_result.get("feature_contributions"),
        confidence_score=prediction_result.get("confidence_score")
    )
    
    db.add(new_prediction)
    db.commit()
    db.refresh(new_prediction)
    
    # Trigger alert if risk is high
    if prediction_result["risk_level"] in [RiskLevel.YELLOW, RiskLevel.RED]:
        from app.services.alert_service import AlertService
        alert_service = AlertService()
        await alert_service.create_alert_from_prediction(new_prediction, db)
    
    return new_prediction


@router.get("/", response_model=List[PredictionResponse])
async def get_predictions(
    timeframe: Optional[PredictionTimeframe] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get predictions for current user"""
    query = db.query(PTSDPrediction).filter(PTSDPrediction.user_id == current_user.id)
    
    if timeframe:
        query = query.filter(PTSDPrediction.timeframe == timeframe)
    
    query = query.order_by(desc(PTSDPrediction.prediction_date))
    
    predictions = query.all()
    return predictions


@router.get("/latest", response_model=PredictionResponse)
async def get_latest_prediction(
    timeframe: PredictionTimeframe = PredictionTimeframe.THIRTY_DAYS,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get latest prediction for user"""
    prediction = db.query(PTSDPrediction).filter(
        PTSDPrediction.user_id == current_user.id,
        PTSDPrediction.timeframe == timeframe
    ).order_by(desc(PTSDPrediction.prediction_date)).first()
    
    if not prediction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No prediction found"
        )
    
    return prediction

