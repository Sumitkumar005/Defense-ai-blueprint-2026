from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.warehouse import Part, InventoryScan
from app.services.computer_vision import ComputerVisionService

router = APIRouter()
cv_service = ComputerVisionService()


@router.get("/parts")
async def get_parts(db: Session = Depends(get_db)):
    """Get all parts"""
    parts = db.query(Part).all()
    return {"parts": parts}


@router.get("/parts/{part_number}")
async def get_part(part_number: str, db: Session = Depends(get_db)):
    """Get part details"""
    part = db.query(Part).filter(Part.part_number == part_number).first()
    if not part:
        return {"error": "Part not found"}
    return part


@router.post("/scan")
async def scan_inventory(
    shelf_location: str,
    image: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """Scan shelf using computer vision"""
    
    # Save uploaded image
    image_path = f"/tmp/{image.filename}"
    with open(image_path, "wb") as f:
        content = await image.read()
        f.write(content)
    
    # Detect parts using CV
    detections = cv_service.detect_parts(image_path)
    
    # Update inventory
    scans = []
    for detection in detections:
        part = db.query(Part).filter(Part.part_number == detection['part_number']).first()
        if part:
            # Update quantity
            part.quantity = detection['quantity']
            part.location = shelf_location
            
            # Create scan record
            scan = InventoryScan(
                part_id=part.id,
                detected_quantity=detection['quantity'],
                confidence_score=detection['confidence'],
                scan_method='camera',
                shelf_location=shelf_location,
                image_url=f"/images/{image.filename}"
            )
            db.add(scan)
            scans.append(scan)
    
    db.commit()
    
    return {
        "scans": len(scans),
        "detections": detections,
        "shelf_location": shelf_location
    }


@router.get("/location/{location}")
async def get_parts_by_location(location: str, db: Session = Depends(get_db)):
    """Get parts at specific location"""
    parts = db.query(Part).filter(Part.location == location).all()
    return {"parts": parts, "location": location}


