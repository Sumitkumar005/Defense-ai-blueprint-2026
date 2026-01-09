"""
Career endpoints
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.career import User
from app.services.mos_translator import MOSTranslator

router = APIRouter()
mos_translator = MOSTranslator()


@router.get("/translate-mos/{mos_code}")
async def translate_mos(mos_code: str):
    """Translate MOS to civilian job titles"""
    job_titles = mos_translator.translate_mos(mos_code)
    return {"mos_code": mos_code, "civilian_job_titles": job_titles}


@router.get("/skills/{user_id}")
async def get_skills(
    user_id: int,
    db: Session = Depends(get_db)
):
    """Extract skills from military experience"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return {"skills": []}
    
    skills = mos_translator.extract_skills(user.military_experience or {})
    return {"skills": skills}
