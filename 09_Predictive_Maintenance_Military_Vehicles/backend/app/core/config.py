from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    APP_NAME: str = "Predictive Maintenance for Military Vehicles"
    DEBUG: bool = False
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    DATABASE_URL: str = "postgresql://user:password@localhost:5432/maintenance_db"
    TIMESCALE_DB_URL: str = "postgresql://user:password@localhost:5432/telematics_db"
    
    SECRET_KEY: str = "CHANGE_THIS_IN_PRODUCTION"
    
    CORS_ORIGINS: List[str] = ["http://localhost:3000"]
    
    # IoT Configuration
    AWS_IOT_ENDPOINT: str = "PLACEHOLDER_IOT_ENDPOINT"
    AWS_IOT_TOPIC: str = "vehicles/telematics"
    
    # ML Service
    ML_SERVICE_URL: str = "http://localhost:8001"
    
    class Config:
        env_file = ".env"


settings = Settings()


