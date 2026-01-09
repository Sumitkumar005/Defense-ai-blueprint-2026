from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    APP_NAME: str = "Smart Sleep Optimization"
    DEBUG: bool = False
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    DATABASE_URL: str = "postgresql://user:password@localhost:5432/sleep_db"
    
    SECRET_KEY: str = "CHANGE_THIS_IN_PRODUCTION"
    ALGORITHM: str = "HS256"
    
    CORS_ORIGINS: List[str] = ["http://localhost:3000"]
    
    # External APIs (Placeholders)
    HEALTHKIT_API_URL: str = "https://api.healthkit.mil/v1"
    GOOGLE_FIT_API_URL: str = "https://api.googlefit.mil/v1"
    
    class Config:
        env_file = ".env"


settings = Settings()

