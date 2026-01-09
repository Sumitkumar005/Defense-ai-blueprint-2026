from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://user:password@localhost:5432/stress_training_db"
    SECRET_KEY: str = "CHANGE_THIS_IN_PRODUCTION"
    
    class Config:
        env_file = ".env"

settings = Settings()

