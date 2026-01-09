"""
ML Prediction Service
Handles PTSD risk prediction using trained models
"""

import numpy as np
import pandas as pd
from typing import List, Dict, Optional
from datetime import datetime, timedelta
from app.models.health_metric import HealthMetric, MetricType
from app.models.prediction import RiskLevel, PredictionTimeframe
from app.core.config import settings
import httpx


class MLPredictionService:
    """Service for ML-based PTSD risk prediction"""
    
    def __init__(self):
        self.model_version = "v1.0.0"
        self.ml_service_url = settings.ML_SERVICE_URL
    
    async def predict_ptsd_risk(
        self,
        user_id: int,
        metrics: List[HealthMetric],
        timeframe: PredictionTimeframe
    ) -> Dict:
        """
        Predict PTSD risk for a user based on health metrics
        
        This is a placeholder implementation. In production, this would:
        1. Extract features from metrics
        2. Call trained ML model (XGBoost + LSTM ensemble)
        3. Return risk score and explainability data
        """
        
        # Feature extraction from metrics
        features = self._extract_features(metrics)
        
        # Call ML model (placeholder - would use actual model in production)
        risk_score = await self._call_ml_model(features, timeframe)
        
        # Determine risk level
        risk_level = self._determine_risk_level(risk_score)
        
        # Calculate feature contributions (for explainability)
        feature_contributions = self._calculate_feature_contributions(features, risk_score)
        
        return {
            "risk_level": risk_level,
            "risk_score": risk_score,
            "model_version": self.model_version,
            "feature_contributions": feature_contributions,
            "confidence_score": 0.85  # Placeholder
        }
    
    def _extract_features(self, metrics: List[HealthMetric]) -> Dict:
        """Extract features from health metrics for ML model"""
        features = {
            "fitness_score_trend": 0.0,
            "sleep_quality_avg": 0.0,
            "social_interaction_frequency": 0.0,
            "training_performance_decline": 0.0,
            "medical_appointment_frequency": 0.0,
            "wellness_checkin_sentiment": 0.0,
            "deployment_stress_score": 0.0,
            "family_separation_duration": 0.0
        }
        
        # Group metrics by type
        metrics_by_type = {}
        for metric in metrics:
            if metric.metric_type not in metrics_by_type:
                metrics_by_type[metric.metric_type] = []
            metrics_by_type[metric.metric_type].append(metric)
        
        # Calculate features from metrics
        if MetricType.FITNESS_SCORE in metrics_by_type:
            fitness_scores = [m.value for m in metrics_by_type[MetricType.FITNESS_SCORE] if m.value]
            if len(fitness_scores) > 1:
                features["fitness_score_trend"] = (fitness_scores[-1] - fitness_scores[0]) / len(fitness_scores)
        
        if MetricType.SLEEP_PATTERN in metrics_by_type:
            sleep_values = [m.value for m in metrics_by_type[MetricType.SLEEP_PATTERN] if m.value]
            if sleep_values:
                features["sleep_quality_avg"] = np.mean(sleep_values)
        
        # Similar processing for other metric types...
        # This is simplified - production would have more sophisticated feature engineering
        
        return features
    
    async def _call_ml_model(self, features: Dict, timeframe: PredictionTimeframe) -> float:
        """
        Call ML model to get risk prediction
        
        PLACEHOLDER: In production, this would:
        1. Load trained model (XGBoost + LSTM ensemble)
        2. Preprocess features
        3. Run inference
        4. Return risk score
        """
        
        # Placeholder: Try to call external ML service, fallback to mock
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.ml_service_url}/predict",
                    json={"features": features, "timeframe": timeframe.value},
                    timeout=5.0
                )
                if response.status_code == 200:
                    result = response.json()
                    return result.get("risk_score", 0.5)
        except:
            pass
        
        # Mock prediction (placeholder)
        # In production, this would use the actual trained model
        base_score = 0.3
        
        # Adjust based on features (simplified logic)
        if features.get("fitness_score_trend", 0) < -0.1:
            base_score += 0.2
        if features.get("sleep_quality_avg", 7.0) < 6.0:
            base_score += 0.15
        if features.get("social_interaction_frequency", 5.0) < 2.0:
            base_score += 0.1
        
        return min(base_score, 1.0)
    
    def _determine_risk_level(self, risk_score: float) -> RiskLevel:
        """Determine risk level from score"""
        if risk_score >= settings.ALERT_RED_THRESHOLD:
            return RiskLevel.RED
        elif risk_score >= settings.ALERT_YELLOW_THRESHOLD:
            return RiskLevel.YELLOW
        else:
            return RiskLevel.GREEN
    
    def _calculate_feature_contributions(self, features: Dict, risk_score: float) -> Dict:
        """Calculate feature contributions for explainability"""
        # Placeholder: In production, would use SHAP values or similar
        contributions = {}
        for feature_name, feature_value in features.items():
            # Simplified contribution calculation
            contributions[feature_name] = {
                "value": feature_value,
                "contribution": abs(feature_value) * 0.1,  # Placeholder
                "direction": "positive" if feature_value > 0 else "negative"
            }
        return contributions

