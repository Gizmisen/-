from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.services.warehouse_service import list_rows

router = APIRouter(prefix="/warehouse", tags=["warehouse"])


@router.get("/health")
def health():
    return {"module": "warehouse", "status": "ready"}


@router.get("/rows")
def rows(limit: int = Query(default=100, ge=1, le=1000), db: Session = Depends(get_db)):
    items = list_rows(db, limit=limit)
    return [{"id": x.id, "material_code": x.material_code, "plant": x.plant, "qty": float(x.qty or 0), "snapshot_date": str(x.snapshot_date) if x.snapshot_date else None} for x in items]
