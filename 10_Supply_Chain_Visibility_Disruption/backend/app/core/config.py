from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    APP_NAME: str = "Supply Chain Visibility & Disruption Prediction"
    DEBUG: bool = False
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    DATABASE_URL: str = "postgresql://user:password@localhost:5432/supply_chain_db"
    NEO4J_URI: str = "bolt://localhost:7687"
    NEO4J_USER: str = "neo4j"
    NEO4J_PASSWORD: str = "password"
    
    SECRET_KEY: str = "CHANGE_THIS_IN_PRODUCTION"
    
    CORS_ORIGINS: List[str] = ["http://localhost:3000"]
    
    # External APIs (Placeholders)
    SUPPLIER_API_URL: str = "PLACEHOLDER_API_URL"
    LOGISTICS_API_URL: str = "PLACEHOLDER_API_URL"
    THREAT_INTELLIGENCE_API: str = "PLACEHOLDER_API_URL"
    
    class Config:
        env_file = ".env"


settings = Settings()


