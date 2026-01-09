"""
Application configuration settings
"""

from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """Application settings"""
    
    # Application
    APP_NAME: str = "Predictive PTSD Early Warning System"
    DEBUG: bool = False
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # Database
    DATABASE_URL: str = "postgresql://user:password@localhost:5432/ptsd_db"
    DATABASE_POOL_SIZE: int = 10
    DATABASE_MAX_OVERFLOW: int = 20
    
    # Security
    SECRET_KEY: str = "CHANGE_THIS_IN_PRODUCTION"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    ENCRYPTION_KEY: str = "CHANGE_THIS_IN_PRODUCTION_32_BYTES"
    
    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8080"]
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # ML Service
    ML_SERVICE_URL: str = "http://localhost:8001"
    ML_MODEL_PATH: str = "./models/ptsd_model.pkl"
    
    # External APIs (Placeholders)
    HEALTH_SYSTEM_API_URL: str = "https://api.healthsystem.mil/v1"
    HEALTH_SYSTEM_API_KEY: str = "PLACEHOLDER_API_KEY"
    TRAINING_DB_API_URL: str = "https://api.training.mil/v1"
    TRAINING_DB_API_KEY: str = "PLACEHOLDER_API_KEY"
    FITNESS_TRACKER_API_URL: str = "https://api.fitness.mil/v1"
    FITNESS_TRACKER_API_KEY: str = "PLACEHOLDER_API_KEY"
    
    # Privacy & Compliance
    FEDERATED_LEARNING_ENABLED: bool = True
    DATA_RETENTION_DAYS: int = 365
    ANONYMIZATION_ENABLED: bool = True
    
    # Alert System
    ALERT_GREEN_THRESHOLD: float = 0.3
    ALERT_YELLOW_THRESHOLD: float = 0.6
    ALERT_RED_THRESHOLD: float = 0.8
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()

