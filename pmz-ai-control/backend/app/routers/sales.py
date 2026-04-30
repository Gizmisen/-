from datetime import date

from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database import get_db
from app.services.sales_service import create_row, list_rows

router = APIRouter(prefix="/sales", tags=["sales"])


class SalesCreate(BaseModel):
    order_number: str
    plant: str | None = None
    quantity: float = 0
    required_date: date | None = None
    status: str | None = None


@router.get("/health")
def health():
    return {"module": "sales", "status": "ready"}


@router.get("/rows")
def rows(limit: int = Query(default=100, ge=1, le=1000), db: Session = Depends(get_db)):
    items = list_rows(db, limit=limit)
    return [{"id": x.id, "order_number": x.order_number, "plant": x.plant, "quantity": float(x.quantity or 0), "required_date": str(x.required_date) if x.required_date else None, "status": x.status} for x in items]


@router.post("/rows")
def add_row(payload: SalesCreate, db: Session = Depends(get_db)):
    x = create_row(db, order_number=payload.order_number, plant=payload.plant, quantity=payload.quantity, required_date=payload.required_date, status=payload.status)
    return {"id": x.id}
