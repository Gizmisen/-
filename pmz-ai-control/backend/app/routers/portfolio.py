from datetime import date

from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.imports import FileImport
from app.models.master_data import PortfolioPlanningVariant
from app.services.portfolio_import_service import import_portfolio_requests
from app.services.portfolio_batch_service import confirm_batch, preview_batch
from app.services.portfolio_transfer_service import confirm_transfers, delete_current_transfers, preview_transfers
from app.services.portfolio_service import count_rows, create_row, get_row, list_rows, update_row
from app.services.portfolio_validation_service import find_duplicates, find_duplicates_smart, find_missing_materials, find_missing_required_fields
from app.services.production_data_service import find_material
from app.services.audit_service import write_audit

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


class MaterialChange(BaseModel):
    new_material_code: str
    reason: str | None = None


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


@router.delete("/{row_id}")
def delete_row(row_id: int, db: Session = Depends(get_db)):
    x = get_row(db, row_id)
    if not x:
        return {"error": "not found"}
    snapshot = serialize(x)
    db.delete(x)
    db.commit()
    write_audit(db, action="portfolio_delete", entity_type="order_portfolio", old_value=snapshot)
    return {"status": "deleted", "id": row_id}


@router.post("/{row_id}/change-material")
def change_material(row_id: int, payload: MaterialChange, db: Session = Depends(get_db)):
    x = get_row(db, row_id)
    if not x:
        return {"error": "not found"}
    material = find_material(db, payload.new_material_code, plant=x.plant)
    if not material:
        return {"error": "material not found in production data for selected plant"}
    old = {"material_code": x.material_code, "material_name": x.material_name}
    x.material_code = material.material_code
    x.material_name = material.material_name
    db.commit()
    db.refresh(x)
    write_audit(db, action="portfolio_change_material", entity_type="order_portfolio", old_value=old, new_value={"material_code": x.material_code, "material_name": x.material_name, "reason": payload.reason})
    return serialize(x)


@router.post("/import/{file_id}")
def import_portfolio(file_id: int, db: Session = Depends(get_db)):
    rec = db.query(FileImport).filter(FileImport.id == file_id).first()
    if not rec:
        return {"error": "file not found"}
    rows = import_portfolio_requests(db, rec)
    return {"status": rec.status, "imported_rows": rows}


@router.get("/batch-preview/{file_id}")
def batch_preview(file_id: int, db: Session = Depends(get_db)):
    rows = preview_batch(db, file_import_id=file_id)
    return {"items": [{"id": x.id, "plant": x.plant, "customer_name": x.customer_name, "planning_variant": x.planning_variant, "order_number": x.order_number, "material_code": x.material_code, "material_name": x.material_name, "variant_qty": float(x.variant_qty or 0), "delivery_date": str(x.delivery_date) if x.delivery_date else None, "status": x.status, "validation_status": x.validation_status} for x in rows]}


@router.post("/batch-confirm/{file_id}")
def batch_confirm(file_id: int, db: Session = Depends(get_db)):
    return confirm_batch(db, file_import_id=file_id)


@router.post("/transfers/preview")
def transfers_preview(db: Session = Depends(get_db)):
    rows = preview_transfers(db)
    batch_id = rows[0].transfer_batch_id if rows else None
    return {"batch_id": batch_id, "items": [{"id": x.id, "transfer_type": x.transfer_type, "plant": x.plant, "material_code": x.material_code, "qty": float(x.qty or 0), "status": x.status} for x in rows]}


@router.post("/transfers/confirm")
def transfers_confirm(batch_id: str, db: Session = Depends(get_db)):
    return {"batch_id": batch_id, "count": confirm_transfers(db, batch_id=batch_id)}


@router.delete("/transfers/current")
def transfers_delete_current(db: Session = Depends(get_db)):
    return {"deleted": delete_current_transfers(db)}


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
