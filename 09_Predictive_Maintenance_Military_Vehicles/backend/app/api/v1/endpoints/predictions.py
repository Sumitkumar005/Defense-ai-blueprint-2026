from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from app.core.database import get_db, get_timescale_db
from app.models.vehicle import FailurePrediction, Vehicle, TelematicsData
from app.services.ml_predictor import MLPredictor

router = APIRouter()
ml_predictor = MLPredictor()


@router.post("/generate/{vehicle_id}")
async def generate_prediction(
    vehicle_id: str,
    component: str = Query(...),
    db: Session = Depends(get_db)
):
    """Generate failure prediction for vehicle component"""
    
    vehicle = db.query(Vehicle).filter(Vehicle.vehicle_id == vehicle_id).first()
    if not vehicle:
        return {"error": "Vehicle not found"}
    
    # Get recent telematics data
    timescale_db = next(get_timescale_db())
    cutoff = datetime.utcnow() - timedelta(days=90)
    telematics = timescale_db.query(TelematicsData).filter(
        TelematicsData.vehicle_id == vehicle_id,
        TelematicsData.timestamp >= cutoff
    ).order_by(TelematicsData.timestamp.desc()).limit(1000).all()
    
    # Convert to dict format
    telematics_data = [
        {
            "engine_temp": t.engine_temp,
            "oil_pressure": t.oil_pressure,
            "coolant_temp": t.coolant_temp,
            "rpm": t.rpm,
            "error_codes": t.error_codes
        }
        for t in telematics
    ]
    
    # Generate prediction
    prediction_result = await ml_predictor.predict_failure(
        vehicle_id=vehicle_id,
        telematics_data=telematics_data,
        component=component
    )
    
    # Save prediction
    prediction = FailurePrediction(
        vehicle_id=vehicle.id,
        component=component,
        failure_probability=prediction_result["failure_probability"],
        predicted_failure_date=datetime.fromisoformat(prediction_result["predicted_failure_date"]),
        timeframe=prediction_result["timeframe"],
        confidence_score=prediction_result["confidence_score"],
        feature_contributions=prediction_result.get("feature_contributions"),
        model_version="v1.0.0"
    )
    
    db.add(prediction)
    db.commit()
    db.refresh(prediction)
    
    return prediction


@router.get("/{vehicle_id}")
async def get_predictions(
    vehicle_id: str,
    db: Session = Depends(get_db)
):
    """Get active predictions for vehicle"""
    vehicle = db.query(Vehicle).filter(Vehicle.vehicle_id == vehicle_id).first()
    if not vehicle:
        return {"error": "Vehicle not found"}
    
    predictions = db.query(FailurePrediction).filter(
        FailurePrediction.vehicle_id == vehicle.id,
        FailurePrediction.is_active == True
    ).order_by(FailurePrediction.failure_probability.desc()).all()
    
    return {"predictions": predictions}
