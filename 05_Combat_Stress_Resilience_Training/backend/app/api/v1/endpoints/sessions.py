from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.training import TrainingSession
from app.services.stress_analyzer import StressAnalyzer

router = APIRouter()
analyzer = StressAnalyzer()

@router.get("/{session_id}")
async def get_session(session_id: int, db: Session = Depends(get_db)):
    """Get training session details"""
    session = db.query(TrainingSession).filter(TrainingSession.id == session_id).first()
    if not session:
        return {"error": "Session not found"}
    return session

@router.post("/{session_id}/complete")
async def complete_session(
    session_id: int,
    biometric_data: dict,
    db: Session = Depends(get_db)
):
    """Complete training session and analyze results"""
    session = db.query(TrainingSession).filter(TrainingSession.id == session_id).first()
    if not session:
        return {"error": "Session not found"}
    
    # Analyze stress response
    baseline = {"resting_heart_rate": 70}  # Would load from database
    analysis = analyzer.analyze_stress_response(baseline, biometric_data)
    
    # Update session
    session.biometric_data = biometric_data
    session.peak_stress_level = analysis['peak_stress_level']
    session.stress_recovery_time = analysis['stress_recovery_time']
    session.decision_quality_score = analysis['decision_quality_score']
    session.ai_feedback = analysis['recommendations']
    
    db.commit()
    
    return {
        "session_id": session_id,
        "analysis": analysis,
        "next_difficulty": analyzer.recommend_next_difficulty(
            session.difficulty_level,
            [analysis]
        )
    }

