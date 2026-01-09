from fastapi import APIRouter
from app.api.v1.endpoints import auth, career, jobs, resume, interview

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(career.router, prefix="/career", tags=["career"])
api_router.include_router(jobs.router, prefix="/jobs", tags=["jobs"])
api_router.include_router(resume.router, prefix="/resume", tags=["resume"])
api_router.include_router(interview.router, prefix="/interview", tags=["interview"])
