from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.warehouse import PickingTask, Part
from pydantic import BaseModel

router = APIRouter()


class PickingTaskCreate(BaseModel):
    order_number: str
    part_number: str
    quantity_requested: int
    picker_id: str = None


@router.post("/task")
async def create_picking_task(
    task: PickingTaskCreate,
    db: Session = Depends(get_db)
):
    """Create picking task with AR guidance"""
    part = db.query(Part).filter(Part.part_number == task.part_number).first()
    if not part:
        return {"error": "Part not found"}
    
    picking_task = PickingTask(
        order_number=task.order_number,
        part_id=part.id,
        quantity_requested=task.quantity_requested,
        picker_id=task.picker_id,
        ar_guidance_enabled=True
    )
    
    db.add(picking_task)
    db.commit()
    db.refresh(picking_task)
    
    return {
        "task_id": picking_task.id,
        "part_number": task.part_number,
        "location": part.location,
        "ar_guidance": {
            "enabled": True,
            "shelf_location": part.location,
            "instructions": f"Navigate to shelf {part.location}, pick {task.quantity_requested} units"
        }
    }


@router.get("/task/{task_id}/guidance")
async def get_ar_guidance(task_id: int, db: Session = Depends(get_db)):
    """Get AR guidance for picking task"""
    task = db.query(PickingTask).filter(PickingTask.id == task_id).first()
    if not task:
        return {"error": "Task not found"}
    
    part = db.query(Part).filter(Part.id == task.part_id).first()
    
    return {
        "task_id": task_id,
        "part_number": part.part_number if part else "Unknown",
        "location": part.location if part else "Unknown",
        "quantity": task.quantity_requested,
        "ar_overlay": {
            "shelf_highlight": part.location if part else None,
            "path_guidance": f"Walk to aisle {part.location.split('-')[0] if part else 'A'}"
        }
    }


