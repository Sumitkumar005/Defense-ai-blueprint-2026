"""
Authentication endpoints (simplified)
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.sleep import User

router = APIRouter()


async def get_current_user(db: Session = Depends(get_db)):
    """Placeholder auth - in production would verify JWT"""
    # For demo, return first user
    user = db.query(User).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

