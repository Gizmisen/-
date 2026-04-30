from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.imports import FileImport
from app.services.orders_history_import_service import import_orders_history
from app.services.orders_history_service import create_row, list_rows
from app.services.orders_history_match_service import compare_with_portfolio, find_analogs

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


@router.post("/import/{file_id}")
def import_history(file_id: int, db: Session = Depends(get_db)):
    rec = db.query(FileImport).filter(FileImport.id == file_id).first()
    if not rec:
        return {"error": "file not found"}
    return import_orders_history(db, rec)


@router.get("/find-analogs")
def analogs(material_code: str | None = Query(default=None), plant: str | None = Query(default=None), limit: int = Query(default=100, ge=1, le=1000), db: Session = Depends(get_db)):
    return {"items": find_analogs(db, material_code=material_code, plant=plant, limit=limit)}


@router.get("/compare-with-portfolio")
def compare_portfolio(limit: int = Query(default=200, ge=1, le=2000), db: Session = Depends(get_db)):
    return {"items": compare_with_portfolio(db, limit=limit)}
