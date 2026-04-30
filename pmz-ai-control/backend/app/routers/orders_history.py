from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.imports import FileImport
from app.services.orders_history_import_service import import_orders_history
from app.services.orders_history_service import create_row, get_row, list_rows
from app.services.orders_history_match_service import compare_with_portfolio, find_analogs, unmatched_history_rows

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


@router.get("/")
def history_list(
    order_number: str | None = Query(default=None),
    material_code: str | None = Query(default=None),
    customer_name: str | None = Query(default=None),
    limit: int = Query(default=100, ge=1, le=1000),
    db: Session = Depends(get_db),
):
    items = list_rows(db, order_number=order_number, material_code=material_code, customer_name=customer_name, limit=limit)
    return {"items": [serialize(x) for x in items]}


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


@router.get("/unmatched")
def unmatched(limit: int = Query(default=200, ge=1, le=2000), db: Session = Depends(get_db)):
    return {"items": unmatched_history_rows(db, limit=limit)}


@router.get("/by-order/{order_number}")
def by_order(order_number: str, db: Session = Depends(get_db)):
    items = list_rows(db, order_number=order_number, limit=1000)
    return {"items": [{"id": x.id, "order_number": x.order_number, "status": x.status, "comment": x.comment} for x in items]}


@router.get("/by-material/{material_code}")
def by_material(material_code: str, db: Session = Depends(get_db)):
    items = find_analogs(db, material_code=material_code, limit=1000)
    return {"items": items}


@router.get("/by-customer/{customer_name}")
def by_customer(customer_name: str, db: Session = Depends(get_db)):
    items = list_rows(db, customer_name=customer_name, limit=1000)
    return {"items": [serialize(x) for x in items]}


@router.get("/{row_id}")
def by_id(row_id: int, db: Session = Depends(get_db)):
    x = get_row(db, row_id)
    if x:
        return serialize(x)
    return {"error": "not found"}


def serialize(x):
    return {
        "id": x.id,
        "source_sheet": x.source_sheet,
        "source_profile": x.source_profile,
        "source_row_number": x.source_row_number,
        "period": x.period,
        "year": x.year,
        "month": x.month,
        "plant": x.plant,
        "customer_name": x.customer_name,
        "registration_number": x.registration_number,
        "order_number": x.order_number,
        "sap_order_number": x.sap_order_number,
        "material_code": x.material_code,
        "material_name": x.material_name,
        "qty_requested": float(x.qty or 0),
        "qty_agreed": float(x.qty_agreed or 0),
        "qty_planned": float(x.qty_planned or 0),
        "qty_fact": float(x.qty_fact or 0),
        "qty_shipped": float(x.qty_shipped or 0),
        "status": x.status,
        "status_group": x.status_group,
        "date_input": str(x.date_input) if x.date_input else None,
        "date_finish_plan": str(x.date_finish_plan) if x.date_finish_plan else None,
        "date_finish_fact": str(x.date_finish_fact) if x.date_finish_fact else None,
        "comment": x.comment,
    }
