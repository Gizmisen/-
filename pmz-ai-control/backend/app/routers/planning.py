from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.services.planning_service import list_rows

router = APIRouter(prefix="/planning", tags=["planning"])


@router.get("/health")
def health():
    return {"module": "planning", "status": "ready"}


@router.get("/rows")
def rows(period: str | None = Query(default=None), limit: int = Query(default=100, ge=1, le=1000), db: Session = Depends(get_db)):
    items = list_rows(db, period=period, limit=limit)
    return [{"id": x.id, "period": x.plan_period, "version": x.plan_version, "order_number": x.order_number, "material_code": x.material_code, "work_center": x.work_center, "planned_qty": float(x.planned_qty or 0), "planned_hours": float(x.planned_hours or 0)} for x in items]
