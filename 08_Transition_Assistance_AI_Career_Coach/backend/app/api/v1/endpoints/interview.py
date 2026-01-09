"""
Interview coaching endpoints
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.core.database import get_db
from app.models.career import InterviewSession, User
from app.services.interview_coach import InterviewCoach

router = APIRouter()
interview_coach = InterviewCoach()


class InterviewAnswer(BaseModel):
    question: str
    answer: str


@router.post("/practice/start")
async def start_interview_practice(
    job_title: str,
    user_id: int = 1,  # PLACEHOLDER: Would get from auth
    db: Session = Depends(get_db)
):
    """Start interview practice session"""
    questions = await interview_coach.generate_questions(job_title)
    
    session = InterviewSession(
        user_id=user_id,
        job_title=job_title,
        questions=questions,
        answers=[]
    )
    db.add(session)
    db.commit()
    db.refresh(session)
    
    return {
        "session_id": session.id,
        "questions": questions
    }


@router.post("/practice/{session_id}/answer")
async def submit_answer(
    session_id: int,
    answer_data: InterviewAnswer,
    db: Session = Depends(get_db)
):
    """Submit interview answer and get feedback"""
    session = db.query(InterviewSession).filter(
        InterviewSession.id == session_id
    ).first()
    
    if not session:
        return {"error": "Session not found"}
    
    # Analyze answer
    feedback = await interview_coach.analyze_answer(
        question=answer_data.question,
        answer=answer_data.answer
    )
    
    # Update session
    if not session.answers:
        session.answers = []
    session.answers.append({
        "question": answer_data.question,
        "answer": answer_data.answer,
        "feedback": feedback
    })
    
    db.commit()
    
    return feedback
