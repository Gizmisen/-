from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.imports import FileImport
from app.services.portfolio_import_service import import_portfolio_requests
from app.services.portfolio_service import create_row, list_rows
from app.services.portfolio_validation_service import find_duplicates, find_missing_materials

router = APIRouter(prefix="/portfolio", tags=["portfolio"])


class PortfolioCreate(BaseModel):
    period: str
    order_number: str
    material_code: str | None = None
    plant: str | None = None
    qty: float = 0


@router.get("/health")
def health():
    return {"module": "portfolio", "status": "ready"}


@router.get("/rows")
def rows(limit: int = Query(default=100, ge=1, le=1000), db: Session = Depends(get_db)):
    items = list_rows(db, limit=limit)
    return [{"id": x.id, "period": x.period, "order_number": x.order_number, "material_code": x.material_code, "plant": x.plant, "qty": float(x.qty or 0)} for x in items]


@router.post("/rows")
def add_row(payload: PortfolioCreate, db: Session = Depends(get_db)):
    x = create_row(db, period=payload.period, order_number=payload.order_number, material_code=payload.material_code, plant=payload.plant, qty=payload.qty)
    return {"id": x.id}


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


@router.get("/missing-materials")
def missing_materials(db: Session = Depends(get_db)):
    return {"items": find_missing_materials(db)}
