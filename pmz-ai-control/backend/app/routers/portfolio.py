from datetime import date

from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.imports import FileImport
from app.models.master_data import PortfolioPlanningVariant
from app.services.portfolio_import_service import import_portfolio_requests
from app.services.portfolio_service import count_rows, create_row, get_row, list_rows, update_row
from app.services.portfolio_validation_service import find_duplicates, find_duplicates_smart, find_missing_materials, find_missing_required_fields

router = APIRouter(prefix="/portfolio", tags=["portfolio"])


class PortfolioCreate(BaseModel):
    period: str
    order_number: str
    material_code: str | None = None
    plant: str | None = None
    qty: float = 0
    customer_name: str | None = None
    planning_variant: str | None = None
    note: str | None = None
    planned_delivery_date: date | None = None


class PortfolioUpdate(BaseModel):
    qty: float | None = None
    note: str | None = None
    planned_delivery_date: date | None = None
    planning_variant: str | None = None
    order_status: str | None = None


@router.get("/health")
def health():
    return {"module": "portfolio", "status": "ready"}


@router.get("/")
def list_portfolio(limit: int = Query(default=100, ge=1, le=1000), db: Session = Depends(get_db)):
    items = list_rows(db, limit=limit)
    return {"items": [serialize(x) for x in items], "total": count_rows(db), "limit": limit, "offset": 0}


@router.get("/rows")
def rows(
    limit: int = Query(default=100, ge=1, le=1000),
    offset: int = Query(default=0, ge=0),
    material_code: str | None = None,
    order_number: str | None = None,
    plant: str | None = None,
    period: str | None = None,
    order_status: str | None = None,
    db: Session = Depends(get_db),
):
    items = list_rows(
        db,
        limit=limit,
        offset=offset,
        material_code=material_code,
        order_number=order_number,
        plant=plant,
        period=period,
        order_status=order_status,
    )
    return {"items": [serialize(x) for x in items], "limit": limit, "offset": offset}


@router.get("/{row_id}")
def get_portfolio_row(row_id: int, db: Session = Depends(get_db)):
    x = get_row(db, row_id)
    if not x:
        return {"error": "not found"}
    return serialize(x)


@router.post("/add")
def add_row_alias(payload: PortfolioCreate, db: Session = Depends(get_db)):
    return add_row(payload, db)


@router.post("/rows")
def add_row(payload: PortfolioCreate, db: Session = Depends(get_db)):
    x = create_row(db, period=payload.period, order_number=payload.order_number, material_code=payload.material_code, plant=payload.plant, qty=payload.qty, customer_name=payload.customer_name, planning_variant=payload.planning_variant, note=payload.note, planned_delivery_date=payload.planned_delivery_date)
    return {"id": x.id}


@router.patch("/{row_id}")
def patch_row(row_id: int, payload: PortfolioUpdate, db: Session = Depends(get_db)):
    x = update_row(db, row_id, payload.model_dump(exclude_none=True))
    if not x:
        return {"error": "not found"}
    return serialize(x)


@router.post("/import/{file_id}")
def import_portfolio(file_id: int, db: Session = Depends(get_db)):
    rec = db.query(FileImport).filter(FileImport.id == file_id).first()
    if not rec:
        return {"error": "file not found"}
    rows = import_portfolio_requests(db, rec)
    return {"status": rec.status, "imported_rows": rows}


@router.get("/check-duplicates")
def check_duplicates(db: Session = Depends(get_db)):
    return {"items": find_duplicates(db)}


@router.get("/check-duplicates-smart")
def check_duplicates_smart(db: Session = Depends(get_db)):
    return {"items": find_duplicates_smart(db)}


@router.get("/missing-materials")
def missing_materials(db: Session = Depends(get_db)):
    return {"items": find_missing_materials(db)}


@router.get("/missing-fields")
def missing_fields(db: Session = Depends(get_db)):
    return {"items": find_missing_required_fields(db)}


@router.get("/planning-variants")
def planning_variants(db: Session = Depends(get_db)):
    rows = db.query(PortfolioPlanningVariant).filter(PortfolioPlanningVariant.is_active.is_(True)).all()
    return {"items": [{"id": x.id, "variant_code": x.variant_code, "variant_name": x.variant_name} for x in rows]}


@router.get("/by-material/{material_code}")
def by_material(material_code: str, db: Session = Depends(get_db)):
    items = list_rows(db, limit=5000, material_code=material_code)
    return {"items": [serialize(x) for x in items]}


@router.get("/by-order/{order_number}")
def by_order(order_number: str, db: Session = Depends(get_db)):
    items = list_rows(db, limit=5000, order_number=order_number)
    return {"items": [serialize(x) for x in items]}


def serialize(x):
    return {
        "id": x.id,
        "period": x.period,
        "plant": x.plant,
        "customer_name": x.customer_name,
        "planning_variant": x.planning_variant,
        "order_number": x.order_number,
        "material_code": x.material_code,
        "material_name": x.material_name,
        "qty": float(x.qty or 0),
        "agreed_qty": float(x.agreed_qty or 0),
        "planned_qty": float(x.planned_qty or 0),
        "shipped_qty": float(x.shipped_qty or 0),
        "note": x.note,
        "planned_delivery_date": str(x.planned_delivery_date) if x.planned_delivery_date else None,
        "order_status": x.order_status,
    }
