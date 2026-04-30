from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.services.sales_service import list_rows

router = APIRouter(prefix="/sales", tags=["sales"])


@router.get("/health")
def health():
    return {"module": "sales", "status": "ready"}


@router.get("/rows")
def rows(limit: int = Query(default=100, ge=1, le=1000), db: Session = Depends(get_db)):
    items = list_rows(db, limit=limit)
    return [{"id": x.id, "order_number": x.order_number, "plant": x.plant, "quantity": float(x.quantity or 0), "required_date": str(x.required_date) if x.required_date else None, "status": x.status} for x in items]
