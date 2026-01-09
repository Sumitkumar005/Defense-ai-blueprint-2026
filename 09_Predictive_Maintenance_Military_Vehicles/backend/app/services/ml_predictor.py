"""
ML Prediction Service for Vehicle Maintenance
"""

import httpx
from typing import Dict, List
from datetime import datetime, timedelta
from app.core.config import settings


class MLPredictor:
    """ML service for failure prediction"""
    
    async def predict_failure(
        self,
        vehicle_id: str,
        telematics_data: List[Dict],
        component: str
    ) -> Dict:
        """
        Predict component failure probability
        
        PLACEHOLDER: In production, would use trained time-series model
        """
        
        # Try ML service
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{settings.ML_SERVICE_URL}/predict",
                    json={
                        "vehicle_id": vehicle_id,
                        "telematics": telematics_data,
                        "component": component
                    },
                    timeout=10.0
                )
                if response.status_code == 200:
                    return response.json()
        except:
            pass
        
        # Fallback: Simple heuristic
        return self._heuristic_prediction(telematics_data, component)
    
    def _heuristic_prediction(self, telematics_data: List[Dict], component: str) -> Dict:
        """Simple heuristic-based prediction"""
        if not telematics_data:
            return {
                "failure_probability": 0.1,
                "predicted_failure_date": (datetime.utcnow() + timedelta(days=90)).isoformat(),
                "confidence_score": 0.5,
                "timeframe": "90_days"
            }
        
        # Analyze recent data
        recent_data = telematics_data[-10:] if len(telematics_data) > 10 else telematics_data
        
        # Simple anomaly detection
        avg_temp = sum(d.get('engine_temp', 0) for d in recent_data) / len(recent_data)
        avg_pressure = sum(d.get('oil_pressure', 0) for d in recent_data) / len(recent_data)
        
        risk_score = 0.2  # Base risk
        
        # High temperature increases risk
        if avg_temp > 220:
            risk_score += 0.3
        if avg_pressure < 30:
            risk_score += 0.3
        
        # Error codes increase risk
        error_count = sum(1 for d in recent_data if d.get('error_codes'))
        if error_count > 0:
            risk_score += min(0.3, error_count * 0.1)
        
        risk_score = min(1.0, risk_score)
        
        # Determine timeframe
        if risk_score > 0.7:
            timeframe = "30_days"
            days = 30
        elif risk_score > 0.5:
            timeframe = "60_days"
            days = 60
        else:
            timeframe = "90_days"
            days = 90
        
        return {
            "failure_probability": risk_score,
            "predicted_failure_date": (datetime.utcnow() + timedelta(days=days)).isoformat(),
            "confidence_score": 0.75,
            "timeframe": timeframe,
            "feature_contributions": {
                "engine_temperature": avg_temp,
                "oil_pressure": avg_pressure,
                "error_codes": error_count
            }
        }


