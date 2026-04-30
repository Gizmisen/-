from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database import get_db
from app.services.master_data_service import (
    create_customer,
    create_plant,
    create_variant,
    create_work_center,
    list_customers,
    list_plants,
    list_variants,
    list_work_centers,
)

router = APIRouter(prefix="/master-data", tags=["master-data"])


class WorkCenterCreate(BaseModel):
    work_center_name: str
    work_center_number: str
    department: str
    plant: str


class CustomerCreate(BaseModel):
    customer_name: str
    customer_code: str | None = None
    short_name: str | None = None
    plant: str | None = None


class PlantCreate(BaseModel):
    plant_code: str
    plant_name: str


class VariantCreate(BaseModel):
    variant_code: str
    variant_name: str
    description: str | None = None


@router.get("/work-centers")
def work_centers(limit: int = Query(default=200, ge=1, le=1000), db: Session = Depends(get_db)):
    return {"items": [serialize_wc(x) for x in list_work_centers(db, limit=limit)]}


@router.post("/work-centers")
def add_work_center(payload: WorkCenterCreate, db: Session = Depends(get_db)):
    x = create_work_center(db, payload.model_dump())
    return {"id": x.id}


@router.get("/customers")
def customers(limit: int = Query(default=200, ge=1, le=1000), db: Session = Depends(get_db)):
    return {"items": [serialize_customer(x) for x in list_customers(db, limit=limit)]}


@router.post("/customers")
def add_customer(payload: CustomerCreate, db: Session = Depends(get_db)):
    x = create_customer(db, payload.model_dump())
    return {"id": x.id}


@router.get("/plants")
def plants(limit: int = Query(default=200, ge=1, le=1000), db: Session = Depends(get_db)):
    return {"items": [serialize_plant(x) for x in list_plants(db, limit=limit)]}


@router.post("/plants")
def add_plant(payload: PlantCreate, db: Session = Depends(get_db)):
    x = create_plant(db, payload.model_dump())
    return {"id": x.id}


@router.get("/planning-variants")
def planning_variants(limit: int = Query(default=200, ge=1, le=1000), db: Session = Depends(get_db)):
    return {"items": [serialize_variant(x) for x in list_variants(db, limit=limit)]}


@router.post("/planning-variants")
def add_planning_variant(payload: VariantCreate, db: Session = Depends(get_db)):
    x = create_variant(db, payload.model_dump())
    return {"id": x.id}


def serialize_wc(x):
    return {"id": x.id, "work_center_name": x.work_center_name, "work_center_number": x.work_center_number, "department": x.department, "plant": x.plant, "is_active": x.is_active}


def serialize_customer(x):
    return {"id": x.id, "customer_code": x.customer_code, "customer_name": x.customer_name, "short_name": x.short_name, "plant": x.plant, "is_active": x.is_active}


def serialize_plant(x):
    return {"id": x.id, "plant_code": x.plant_code, "plant_name": x.plant_name, "is_active": x.is_active}


def serialize_variant(x):
    return {"id": x.id, "variant_code": x.variant_code, "variant_name": x.variant_name, "description": x.description, "is_active": x.is_active}
