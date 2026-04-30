from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.services.dashboard_service import build_dashboard

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/health")
def health():
    return {"module": "dashboard", "status": "ready"}


@router.get("/summary")
def summary(db: Session = Depends(get_db)):
    return build_dashboard(db)
