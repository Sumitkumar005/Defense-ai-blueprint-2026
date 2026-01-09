"""
Supply Chain Disruption Prediction Service
"""

import httpx
from typing import Dict, List
from datetime import datetime, timedelta
from app.core.config import settings


class DisruptionPredictor:
    """Predict supply chain disruptions"""
    
    async def predict_disruption(
        self,
        component_id: int,
        supplier_id: int,
        supplier_data: Dict,
        external_factors: Dict
    ) -> Dict:
        """
        Predict supply chain disruption
        
        PLACEHOLDER: In production, would use ML model considering:
        - Supplier financial health
        - Geopolitical risks
        - Historical performance
        - Weather patterns
        - Cyber threat intelligence
        """
        
        # Try ML service
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{settings.ML_SERVICE_URL}/predict-disruption",
                    json={
                        "component_id": component_id,
                        "supplier_id": supplier_id,
                        "supplier_data": supplier_data,
                        "external_factors": external_factors
                    },
                    timeout=10.0
                )
                if response.status_code == 200:
                    return response.json()
        except:
            pass
        
        # Fallback: Risk-based prediction
        return self._risk_based_prediction(supplier_data, external_factors)
    
    def _risk_based_prediction(self, supplier_data: Dict, external_factors: Dict) -> Dict:
        """Simple risk-based prediction"""
        risk_score = 0.2  # Base risk
        
        # Supplier reliability
        reliability = supplier_data.get('reliability_score', 0.5)
        if reliability < 0.3:
            risk_score += 0.4
        
        # Geopolitical risk
        geo_risk = external_factors.get('geopolitical_risk', 0.0)
        risk_score += geo_risk * 0.3
        
        # Financial health
        financial_health = supplier_data.get('financial_health', 0.5)
        if financial_health < 0.3:
            risk_score += 0.2
        
        risk_score = min(1.0, risk_score)
        
        # Determine disruption type
        if geo_risk > 0.5:
            disruption_type = "geopolitical"
        elif supplier_data.get('cyber_threats', 0) > 0.5:
            disruption_type = "cyber"
        elif external_factors.get('natural_disaster_risk', 0) > 0.5:
            disruption_type = "natural_disaster"
        else:
            disruption_type = "supplier_failure"
        
        return {
            "disruption_probability": risk_score,
            "predicted_disruption_date": (datetime.utcnow() + timedelta(days=60)).isoformat(),
            "disruption_type": disruption_type,
            "impact_severity": "high" if risk_score > 0.7 else "medium" if risk_score > 0.4 else "low",
            "mitigation_strategies": [
                "Identify alternative suppliers",
                "Increase safety stock",
                "Monitor supplier financial health"
            ]
        }


