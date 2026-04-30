from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.services.production_data_service import get_summary

router = APIRouter(prefix="/production-data", tags=["production-data"])


@router.get("/health")
def health():
    return {"module": "production_data", "status": "ready"}


@router.get("/summary")
def summary(db: Session = Depends(get_db)):
    return get_summary(db)
