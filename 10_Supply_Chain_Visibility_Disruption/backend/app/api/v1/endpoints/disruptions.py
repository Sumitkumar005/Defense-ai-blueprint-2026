from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from datetime import datetime
from app.core.database import get_db
from app.models.supply_chain import DisruptionPrediction, Component, Supplier
from app.services.disruption_predictor import DisruptionPredictor

router = APIRouter()
predictor = DisruptionPredictor()


@router.post("/predict")
async def predict_disruption(
    component_id: int,
    supplier_id: int,
    db: Session = Depends(get_db)
):
    """Generate disruption prediction"""
    
    component = db.query(Component).filter(Component.id == component_id).first()
    supplier = db.query(Supplier).filter(Supplier.id == supplier_id).first()
    
    if not component or not supplier:
        return {"error": "Component or supplier not found"}
    
    # Get supplier data
    supplier_data = {
        "reliability_score": supplier.reliability_score,
        "quality_score": supplier.quality_score,
        "delivery_performance": supplier.delivery_performance,
        "financial_health": 0.5,  # Would fetch from external API
        "cyber_threats": 0.0  # Would fetch from threat intel
    }
    
    external_factors = {
        "geopolitical_risk": 0.3,  # Would fetch from external API
        "natural_disaster_risk": 0.1  # Would fetch from weather API
    }
    
    # Generate prediction
    prediction_result = await predictor.predict_disruption(
        component_id=component_id,
        supplier_id=supplier_id,
        supplier_data=supplier_data,
        external_factors=external_factors
    )
    
    # Save prediction
    prediction = DisruptionPrediction(
        component_id=component_id,
        supplier_id=supplier_id,
        disruption_probability=prediction_result["disruption_probability"],
        predicted_disruption_date=datetime.fromisoformat(prediction_result["predicted_disruption_date"]),
        disruption_type=prediction_result["disruption_type"],
        impact_severity=prediction_result["impact_severity"],
        mitigation_strategies=prediction_result["mitigation_strategies"]
    )
    
    db.add(prediction)
    db.commit()
    db.refresh(prediction)
    
    return prediction


@router.get("/active")
async def get_active_disruptions(db: Session = Depends(get_db)):
    """Get active disruption predictions"""
    predictions = db.query(DisruptionPrediction).filter(
        DisruptionPrediction.is_active == True
    ).order_by(DisruptionPrediction.disruption_probability.desc()).limit(50).all()
    
    return {"disruptions": predictions}
