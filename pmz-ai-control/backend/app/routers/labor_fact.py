from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database import get_db
from app.services.labor_fact_service import create_row, list_rows

router = APIRouter(prefix="/labor-fact", tags=["labor-fact"])


class LaborFactCreate(BaseModel):
    period: str
    order_number: str
    work_center: str | None = None
    labor_hours: float = 0


@router.get("/health")
def health():
    return {"module": "labor_fact", "status": "ready"}


@router.get("/rows")
def rows(period: str | None = Query(default=None), limit: int = Query(default=100, ge=1, le=1000), db: Session = Depends(get_db)):
    items = list_rows(db, period=period, limit=limit)
    return [{"id": x.id, "period": x.period, "order_number": x.order_number, "work_center": x.work_center, "labor_hours": float(x.labor_hours or 0)} for x in items]


@router.post("/rows")
def add_row(payload: LaborFactCreate, db: Session = Depends(get_db)):
    x = create_row(db, period=payload.period, order_number=payload.order_number, work_center=payload.work_center, labor_hours=payload.labor_hours)
    return {"id": x.id}
