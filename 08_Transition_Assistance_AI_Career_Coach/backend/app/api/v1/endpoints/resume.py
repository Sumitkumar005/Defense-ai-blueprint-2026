"""
Resume endpoints
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.core.database import get_db
from app.models.career import Resume, User
from app.services.resume_builder import ResumeBuilder
from app.services.mos_translator import MOSTranslator

router = APIRouter()
resume_builder = ResumeBuilder()
mos_translator = MOSTranslator()


class ResumeRequest(BaseModel):
    target_job_title: str


@router.post("/generate")
async def generate_resume(
    request: ResumeRequest,
    user_id: int = 1,  # PLACEHOLDER: Would get from auth
    db: Session = Depends(get_db)
):
    """Generate AI resume"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    resume_content = await resume_builder.generate_resume(
        user_id=user_id,
        military_experience=user.military_experience or {},
        target_job_title=request.target_job_title
    )
    
    resume = Resume(
        user_id=user_id,
        content=resume_content,
        target_job_title=request.target_job_title
    )
    db.add(resume)
    db.commit()
    db.refresh(resume)
    
    return {"resume_id": resume.id, "content": resume_content}


@router.get("/{resume_id}")
async def get_resume(resume_id: int, db: Session = Depends(get_db)):
    """Get resume"""
    resume = db.query(Resume).filter(Resume.id == resume_id).first()
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")
    return resume
