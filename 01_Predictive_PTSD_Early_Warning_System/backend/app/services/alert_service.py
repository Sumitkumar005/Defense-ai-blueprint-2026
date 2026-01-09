"""
Alert Service
Handles alert creation and management
"""

from typing import Dict
from sqlalchemy.orm import Session
from app.models.alert import Alert, AlertSeverity, AlertStatus
from app.models.prediction import PTSDPrediction, RiskLevel
from app.core.config import settings


class AlertService:
    """Service for managing alerts"""
    
    async def create_alert_from_prediction(
        self,
        prediction: PTSDPrediction,
        db: Session
    ) -> Alert:
        """Create alert from prediction if risk is elevated"""
        
        # Map risk level to alert severity
        severity_map = {
            RiskLevel.GREEN: AlertSeverity.GREEN,
            RiskLevel.YELLOW: AlertSeverity.YELLOW,
            RiskLevel.RED: AlertSeverity.RED
        }
        
        severity = severity_map.get(prediction.risk_level, AlertSeverity.YELLOW)
        
        # Only create alerts for yellow/red
        if prediction.risk_level == RiskLevel.GREEN:
            return None
        
        # Generate alert message and recommendations
        title, message, recommendations = self._generate_alert_content(
            prediction.risk_level,
            prediction.risk_score,
            prediction.timeframe
        )
        
        # Check if active alert already exists
        existing_alert = db.query(Alert).filter(
            Alert.user_id == prediction.user_id,
            Alert.is_active == True,
            Alert.severity == severity
        ).first()
        
        if existing_alert:
            # Update existing alert
            existing_alert.message = message
            existing_alert.intervention_recommendations = recommendations
            db.commit()
            return existing_alert
        
        # Create new alert
        new_alert = Alert(
            user_id=prediction.user_id,
            severity=severity,
            status=AlertStatus.PENDING,
            title=title,
            message=message,
            intervention_recommendations=recommendations
        )
        
        db.add(new_alert)
        db.commit()
        db.refresh(new_alert)
        
        return new_alert
    
    def _generate_alert_content(
        self,
        risk_level: RiskLevel,
        risk_score: float,
        timeframe: str
    ) -> tuple:
        """Generate alert title, message, and recommendations"""
        
        if risk_level == RiskLevel.RED:
            title = "High Risk Alert - Immediate Attention Recommended"
            message = f"Elevated PTSD risk detected ({risk_score:.1%}) for {timeframe.replace('_', ' ')} timeframe. Immediate intervention recommended."
            recommendations = """
            - Contact mental health coordinator immediately
            - Schedule confidential counseling session
            - Connect with peer support resources
            - Consider chaplain services
            - Review deployment status and stressors
            """
        else:  # YELLOW
            title = "Moderate Risk Alert - Monitoring Recommended"
            message = f"Moderate PTSD risk detected ({risk_score:.1%}) for {timeframe.replace('_', ' ')} timeframe. Proactive monitoring and support recommended."
            recommendations = """
            - Schedule wellness check-in with unit leader
            - Review available mental health resources
            - Consider peer support group participation
            - Monitor stress indicators closely
            - Maintain regular check-ins
            """
        
        return title, message, recommendations

