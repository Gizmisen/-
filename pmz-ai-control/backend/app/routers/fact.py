from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.services.fact_service import list_rows

router = APIRouter(prefix="/fact", tags=["fact"])


@router.get("/health")
def health():
    return {"module": "fact", "status": "ready"}


@router.get("/rows")
def rows(period: str | None = Query(default=None), limit: int = Query(default=100, ge=1, le=1000), db: Session = Depends(get_db)):
    items = list_rows(db, period=period, limit=limit)
    return [{"id": x.id, "period": x.fact_period, "order_number": x.order_number, "material_code": x.material_code, "work_center": x.work_center, "fact_qty": float(x.fact_qty or 0), "fact_hours": float(x.fact_hours or 0)} for x in items]
