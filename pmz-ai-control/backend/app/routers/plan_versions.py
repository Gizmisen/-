from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database import get_db
from app.services.plan_versions_service import add_row, compare_versions, create_version

router = APIRouter(prefix="/plan-versions", tags=["plan-versions"])


class VersionCreate(BaseModel):
    period: str
    version_code: str
    is_active: bool = True


class VersionRowCreate(BaseModel):
    plan_version_id: int
    order_number: str
    material_code: str | None = None
    work_center: str | None = None
    planned_qty: float = 0
    planned_hours: float = 0


class CompareRequest(BaseModel):
    left_version_id: int
    right_version_id: int


@router.get("/health")
def health():
    return {"module": "plan_versions", "status": "ready"}


@router.post("/versions")
def add_version(payload: VersionCreate, db: Session = Depends(get_db)):
    x = create_version(db, period=payload.period, version_code=payload.version_code, is_active=payload.is_active)
    return {"id": x.id}


@router.post("/rows")
def add_version_row(payload: VersionRowCreate, db: Session = Depends(get_db)):
    x = add_row(db, plan_version_id=payload.plan_version_id, order_number=payload.order_number, material_code=payload.material_code, work_center=payload.work_center, planned_qty=payload.planned_qty, planned_hours=payload.planned_hours)
    return {"id": x.id}


@router.post("/compare")
def compare(payload: CompareRequest, db: Session = Depends(get_db)):
    return compare_versions(db, left_version_id=payload.left_version_id, right_version_id=payload.right_version_id)
