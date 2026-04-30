from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database import get_db
from app.services.planning_service import create_row, list_rows

router = APIRouter(prefix="/planning", tags=["planning"])


class PlanningCreate(BaseModel):
    plan_period: str
    plan_version: str = "BP"
    order_number: str
    material_code: str | None = None
    work_center: str | None = None
    planned_qty: float = 0
    planned_hours: float = 0


@router.get("/health")
def health():
    return {"module": "planning", "status": "ready"}


@router.get("/rows")
def rows(period: str | None = Query(default=None), limit: int = Query(default=100, ge=1, le=1000), db: Session = Depends(get_db)):
    items = list_rows(db, period=period, limit=limit)
    return [{"id": x.id, "period": x.plan_period, "version": x.plan_version, "order_number": x.order_number, "material_code": x.material_code, "work_center": x.work_center, "planned_qty": float(x.planned_qty or 0), "planned_hours": float(x.planned_hours or 0)} for x in items]


@router.post("/rows")
def add_row(payload: PlanningCreate, db: Session = Depends(get_db)):
    x = create_row(db, plan_period=payload.plan_period, plan_version=payload.plan_version, order_number=payload.order_number, material_code=payload.material_code, work_center=payload.work_center, planned_qty=payload.planned_qty, planned_hours=payload.planned_hours)
    return {"id": x.id}
