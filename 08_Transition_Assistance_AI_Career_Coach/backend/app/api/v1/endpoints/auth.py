"""
Authentication endpoints (simplified)
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.career import User

router = APIRouter()


async def get_current_user(db: Session = Depends(get_db)):
    """Placeholder auth"""
    user = db.query(User).first()
    return user
