"""
Data Ingestion Service
Handles integration with external systems for passive monitoring
"""

import httpx
from typing import List, Dict
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.core.config import settings
from app.models.health_metric import HealthMetric, MetricType
from app.models.user import User


class DataIngestionService:
    """Service for ingesting data from external systems"""
    
    async def ingest_fitness_tracker_data(
        self,
        user_id: int,
        db: Session
    ) -> List[HealthMetric]:
        """
        Ingest fitness tracker data (sleep, activity, heart rate)
        
        PLACEHOLDER: In production, this would integrate with:
        - Apple HealthKit
        - Garmin Connect
        - WHOOP API
        - Military fitness tracking systems
        """
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{settings.FITNESS_TRACKER_API_URL}/users/{user_id}/metrics",
                    headers={"Authorization": f"Bearer {settings.FITNESS_TRACKER_API_KEY}"},
                    timeout=10.0
                )
                
                if response.status_code == 200:
                    data = response.json()
                    metrics = []
                    
                    # Process sleep data
                    if "sleep" in data:
                        for sleep_record in data["sleep"]:
                            metric = HealthMetric(
                                user_id=user_id,
                                metric_type=MetricType.SLEEP_PATTERN,
                                value=sleep_record.get("quality_score"),
                                metadata={
                                    "duration_hours": sleep_record.get("duration"),
                                    "deep_sleep_minutes": sleep_record.get("deep_sleep"),
                                    "date": sleep_record.get("date")
                                },
                                source="fitness_tracker"
                            )
                            metrics.append(metric)
                    
                    # Process activity data
                    if "activity" in data:
                        for activity_record in data["activity"]:
                            metric = HealthMetric(
                                user_id=user_id,
                                metric_type=MetricType.FITNESS_SCORE,
                                value=activity_record.get("fitness_score"),
                                metadata={
                                    "steps": activity_record.get("steps"),
                                    "calories": activity_record.get("calories"),
                                    "date": activity_record.get("date")
                                },
                                source="fitness_tracker"
                            )
                            metrics.append(metric)
                    
                    # Save to database
                    for metric in metrics:
                        db.add(metric)
                    db.commit()
                    
                    return metrics
        except Exception as e:
            # Log error in production
            print(f"Error ingesting fitness tracker data: {e}")
            return []
        
        # Fallback: return empty list
        return []
    
    async def ingest_training_performance_data(
        self,
        user_id: int,
        db: Session
    ) -> List[HealthMetric]:
        """
        Ingest training performance data
        
        PLACEHOLDER: In production, would integrate with training databases
        """
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{settings.TRAINING_DB_API_URL}/users/{user_id}/performance",
                    headers={"Authorization": f"Bearer {settings.TRAINING_DB_API_KEY}"},
                    timeout=10.0
                )
                
                if response.status_code == 200:
                    data = response.json()
                    metrics = []
                    
                    for record in data.get("performance_records", []):
                        metric = HealthMetric(
                            user_id=user_id,
                            metric_type=MetricType.TRAINING_PERFORMANCE,
                            value=record.get("performance_score"),
                            metadata={
                                "training_type": record.get("type"),
                                "date": record.get("date"),
                                "decline_percentage": record.get("decline")
                            },
                            source="training_database"
                        )
                        metrics.append(metric)
                    
                    for metric in metrics:
                        db.add(metric)
                    db.commit()
                    
                    return metrics
        except Exception as e:
            print(f"Error ingesting training data: {e}")
            return []
        
        return []
    
    async def ingest_health_system_data(
        self,
        user_id: int,
        db: Session
    ) -> List[HealthMetric]:
        """
        Ingest medical appointment and health system data
        
        PLACEHOLDER: In production, would integrate with military health systems
        """
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{settings.HEALTH_SYSTEM_API_URL}/patients/{user_id}/appointments",
                    headers={"Authorization": f"Bearer {settings.HEALTH_SYSTEM_API_KEY}"},
                    timeout=10.0
                )
                
                if response.status_code == 200:
                    data = response.json()
                    metrics = []
                    
                    # Calculate appointment frequency
                    appointments = data.get("appointments", [])
                    if appointments:
                        recent_appointments = [
                            a for a in appointments
                            if datetime.fromisoformat(a["date"]) > datetime.utcnow() - timedelta(days=90)
                        ]
                        frequency = len(recent_appointments) / 90.0  # appointments per day
                        
                        metric = HealthMetric(
                            user_id=user_id,
                            metric_type=MetricType.MEDICAL_APPOINTMENT,
                            value=frequency,
                            metadata={
                                "total_appointments": len(recent_appointments),
                                "appointment_types": [a["type"] for a in recent_appointments]
                            },
                            source="health_system"
                        )
                        metrics.append(metric)
                    
                    for metric in metrics:
                        db.add(metric)
                    db.commit()
                    
                    return metrics
        except Exception as e:
            print(f"Error ingesting health system data: {e}")
            return []
        
        return []

