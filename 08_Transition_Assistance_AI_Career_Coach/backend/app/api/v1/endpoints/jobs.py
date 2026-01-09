"""
Job matching endpoints
"""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.career import JobMatch, User
from app.services.job_matcher import JobMatcher
from app.services.mos_translator import MOSTranslator

router = APIRouter()
job_matcher = JobMatcher()
mos_translator = MOSTranslator()


@router.get("/search")
async def search_jobs(
    job_title: str = Query(None),
    location: str = Query(None),
    user_id: int = 1,  # PLACEHOLDER: Would get from auth
    db: Session = Depends(get_db)
):
    """Search for jobs"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return {"jobs": []}
    
    # Extract skills from military experience
    skills = mos_translator.extract_skills(user.military_experience or {})
    
    # Find jobs
    jobs = await job_matcher.find_jobs(
        skills=skills,
        location=location,
        job_title=job_title
    )
    
    # Save matches
    for job in jobs:
        match = JobMatch(
            user_id=user_id,
            job_title=job.get('title'),
            company=job.get('company'),
            match_score=job.get('match_score', 0),
            job_url=job.get('url'),
            source=job.get('source', 'unknown')
        )
        db.add(match)
    
    db.commit()
    
    return {"jobs": jobs}


@router.get("/matches")
async def get_job_matches(
    user_id: int = 1,  # PLACEHOLDER: Would get from auth
    db: Session = Depends(get_db)
):
    """Get saved job matches"""
    matches = db.query(JobMatch).filter(
        JobMatch.user_id == user_id
    ).order_by(JobMatch.match_score.desc()).limit(20).all()
    
    return {"matches": matches}
