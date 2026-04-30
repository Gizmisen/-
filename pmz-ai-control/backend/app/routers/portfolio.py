from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.services.portfolio_service import list_rows

router = APIRouter(prefix="/portfolio", tags=["portfolio"])


@router.get("/health")
def health():
    return {"module": "portfolio", "status": "ready"}


@router.get("/rows")
def rows(limit: int = Query(default=100, ge=1, le=1000), db: Session = Depends(get_db)):
    items = list_rows(db, limit=limit)
    return [{"id": x.id, "period": x.period, "order_number": x.order_number, "material_code": x.material_code, "plant": x.plant, "qty": float(x.qty or 0)} for x in items]
