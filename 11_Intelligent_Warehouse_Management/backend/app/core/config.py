from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    APP_NAME: str = "Intelligent Warehouse Management"
    DEBUG: bool = False
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    DATABASE_URL: str = "postgresql://user:password@localhost:5432/warehouse_db"
    REDIS_URL: str = "redis://localhost:6379/0"
    
    SECRET_KEY: str = "CHANGE_THIS_IN_PRODUCTION"
    
    CORS_ORIGINS: List[str] = ["http://localhost:3000"]
    
    # Computer Vision
    CV_MODEL_PATH: str = "./models/yolov8_warehouse.pt"
    CV_CONFIDENCE_THRESHOLD: float = 0.5
    
    class Config:
        env_file = ".env"


settings = Settings()


