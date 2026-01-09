from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    APP_NAME: str = "Transition Assistance AI Career Coach"
    DEBUG: bool = False
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    DATABASE_URL: str = "postgresql://user:password@localhost:5432/career_coach_db"
    
    SECRET_KEY: str = "CHANGE_THIS_IN_PRODUCTION"
    ALGORITHM: str = "HS256"
    
    CORS_ORIGINS: List[str] = ["http://localhost:3000"]
    
    # External APIs (Placeholders)
    OPENAI_API_KEY: str = "PLACEHOLDER_API_KEY"
    LINKEDIN_API_KEY: str = "PLACEHOLDER_API_KEY"
    INDEED_API_KEY: str = "PLACEHOLDER_API_KEY"
    USAJOBS_API_KEY: str = "PLACEHOLDER_API_KEY"
    
    class Config:
        env_file = ".env"


settings = Settings()
