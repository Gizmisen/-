from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database import get_db
from app.services.orders_history_service import create_row, list_rows

router = APIRouter(prefix="/orders-history", tags=["orders-history"])


class HistoryCreate(BaseModel):
    order_number: str
    status: str | None = None
    comment: str | None = None


@router.get("/health")
def health():
    return {"module": "orders_history", "status": "ready"}


@router.get("/rows")
def rows(order_number: str | None = Query(default=None), limit: int = Query(default=100, ge=1, le=1000), db: Session = Depends(get_db)):
    items = list_rows(db, order_number=order_number, limit=limit)
    return [{"id": x.id, "order_number": x.order_number, "status": x.status, "comment": x.comment} for x in items]


@router.post("/rows")
def add_row(payload: HistoryCreate, db: Session = Depends(get_db)):
    x = create_row(db, order_number=payload.order_number, status=payload.status, comment=payload.comment)
    return {"id": x.id}
