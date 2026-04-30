from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.materials import Material
from app.services.ai_service import find_material_usage

router = APIRouter(prefix="/materials", tags=["materials"])


@router.get("/{material_code}/card")
def material_card(material_code: str, db: Session = Depends(get_db)):
    material = db.query(Material).filter(Material.material_code == material_code).first()
    if not material:
        raise HTTPException(status_code=404, detail="Material not found")
    usage = find_material_usage(db, material_code)
    return {
        "material_code": material.material_code,
        "material_name": material.material_name,
        "plant": material.plant,
        "unit": material.unit,
        "usage": usage,
    }
