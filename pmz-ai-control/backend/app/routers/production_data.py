from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database import get_db
from app.services.production_data_service import create_material, get_summary, list_materials

router = APIRouter(prefix="/production-data", tags=["production-data"])


class MaterialCreate(BaseModel):
    material_code: str
    material_name: str
    unit: str | None = None
    plant: str | None = None


@router.get("/health")
def health():
    return {"module": "production_data", "status": "ready"}


@router.get("/summary")
def summary(db: Session = Depends(get_db)):
    return get_summary(db)


@router.get("/materials")
def materials(limit: int = Query(default=100, ge=1, le=1000), db: Session = Depends(get_db)):
    items = list_materials(db, limit=limit)
    return [{"id": x.id, "material_code": x.material_code, "material_name": x.material_name, "unit": x.unit, "plant": x.plant} for x in items]


@router.post("/materials")
def add_material(payload: MaterialCreate, db: Session = Depends(get_db)):
    x = create_material(db, material_code=payload.material_code, material_name=payload.material_name, unit=payload.unit, plant=payload.plant)
    return {"id": x.id}
