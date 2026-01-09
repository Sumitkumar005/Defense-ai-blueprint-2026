from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# Main database for metadata
engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# TimescaleDB for time-series telematics data
timescale_engine = create_engine(settings.TIMESCALE_DB_URL)
TimescaleSession = sessionmaker(autocommit=False, autoflush=False, bind=timescale_engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_timescale_db():
    db = TimescaleSession()
    try:
        yield db
    finally:
        db.close()


