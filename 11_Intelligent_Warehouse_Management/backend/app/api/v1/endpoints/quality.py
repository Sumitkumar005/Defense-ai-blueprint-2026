from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.warehouse import QualityInspection, Part
from app.services.computer_vision import ComputerVisionService

router = APIRouter()
cv_service = ComputerVisionService()


@router.post("/inspect")
async def inspect_part(
    part_number: str,
    image: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """Inspect part quality using computer vision"""
    
    part = db.query(Part).filter(Part.part_number == part_number).first()
    if not part:
        return {"error": "Part not found"}
    
    # Save image
    image_path = f"/tmp/{image.filename}"
    with open(image_path, "wb") as f:
        content = await image.read()
        f.write(content)
    
    # Analyze quality
    quality_result = cv_service.analyze_form_quality(image_path, part_number)
    
    # Create inspection record
    inspection = QualityInspection(
        part_id=part.id,
        inspection_type="cv_automated",
        passed=quality_result["passed"],
        defects_detected=quality_result.get("defects", []),
        inspector_id="cv_system"
    )
    
    db.add(inspection)
    db.commit()
    db.refresh(inspection)
    
    return {
        "inspection_id": inspection.id,
        "part_number": part_number,
        "passed": quality_result["passed"],
        "quality_score": quality_result["quality_score"],
        "defects": quality_result.get("defects", []),
        "recommendations": quality_result.get("recommendations", [])
    }


