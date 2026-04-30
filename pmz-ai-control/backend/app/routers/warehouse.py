from datetime import date

from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database import get_db
from app.services.warehouse_service import create_row, list_rows

router = APIRouter(prefix="/warehouse", tags=["warehouse"])


class WarehouseCreate(BaseModel):
    material_code: str
    plant: str | None = None
    qty: float = 0
    snapshot_date: date | None = None


@router.get("/health")
def health():
    return {"module": "warehouse", "status": "ready"}


@router.get("/rows")
def rows(limit: int = Query(default=100, ge=1, le=1000), db: Session = Depends(get_db)):
    items = list_rows(db, limit=limit)
    return [{"id": x.id, "material_code": x.material_code, "plant": x.plant, "qty": float(x.qty or 0), "snapshot_date": str(x.snapshot_date) if x.snapshot_date else None} for x in items]


@router.post("/rows")
def add_row(payload: WarehouseCreate, db: Session = Depends(get_db)):
    x = create_row(db, material_code=payload.material_code, plant=payload.plant, qty=payload.qty, snapshot_date=payload.snapshot_date)
    return {"id": x.id}
