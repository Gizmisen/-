from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database import get_db
from app.services.production_data_service import (
    create_material,
    create_routing,
    create_spec,
    get_summary,
    list_materials,
    list_routings,
    list_specs,
)

router = APIRouter(prefix="/production-data", tags=["production-data"])


class MaterialCreate(BaseModel):
    material_code: str
    material_name: str
    unit: str | None = None
    plant: str | None = None


class SpecCreate(BaseModel):
    parent_material_code: str
    plant: str | None = None
    component_code: str
    component_qty: float = 0
    component_unit: str | None = None


class RoutingCreate(BaseModel):
    material_code: str
    plant: str | None = None
    work_center: str
    labor_value: float = 0
    labor_unit: str | None = "h"


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


@router.get("/specs")
def specs(limit: int = Query(default=100, ge=1, le=1000), db: Session = Depends(get_db)):
    items = list_specs(db, limit=limit)
    return [{"id": x.id, "parent_material_code": x.parent_material_code, "plant": x.plant, "component_code": x.component_code, "component_qty": float(x.component_qty or 0), "component_unit": x.component_unit} for x in items]


@router.post("/specs")
def add_spec(payload: SpecCreate, db: Session = Depends(get_db)):
    x = create_spec(db, parent_material_code=payload.parent_material_code, plant=payload.plant, component_code=payload.component_code, component_qty=payload.component_qty, component_unit=payload.component_unit)
    return {"id": x.id}


@router.get("/routings")
def routings(limit: int = Query(default=100, ge=1, le=1000), db: Session = Depends(get_db)):
    items = list_routings(db, limit=limit)
    return [{"id": x.id, "material_code": x.material_code, "plant": x.plant, "work_center": x.work_center, "labor_value": float(x.labor_value or 0), "labor_unit": x.labor_unit} for x in items]


@router.post("/routings")
def add_routing(payload: RoutingCreate, db: Session = Depends(get_db)):
    x = create_routing(db, material_code=payload.material_code, plant=payload.plant, work_center=payload.work_center, labor_value=payload.labor_value, labor_unit=payload.labor_unit)
    return {"id": x.id}
