from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db

router = APIRouter()

@router.get("/scenarios")
async def get_scenarios():
    """Get available training scenarios"""
    return {
        "scenarios": [
            {"id": 1, "type": "ied_attack", "name": "IED Attack", "difficulty_range": [1, 5]},
            {"id": 2, "type": "ambush", "name": "Ambush Scenario", "difficulty_range": [3, 7]},
            {"id": 3, "type": "casualty", "name": "Casualty Response", "difficulty_range": [5, 10]},
        ]
    }

@router.post("/start")
async def start_training(
    scenario_type: str,
    difficulty: int,
    db: Session = Depends(get_db)
):
    """Start a new training session"""
    # PLACEHOLDER: Would create session and connect to VR
    return {
        "session_id": "mock-session-id",
        "status": "started",
        "scenario_type": scenario_type,
        "difficulty": difficulty
    }

