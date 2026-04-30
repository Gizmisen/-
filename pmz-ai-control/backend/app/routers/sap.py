from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.services.sap_service import summary

router = APIRouter(prefix="/sap", tags=["sap"])


@router.get("/health")
def health():
    return {"module": "sap", "status": "ready"}


@router.get("/summary")
def sap_summary(db: Session = Depends(get_db)):
    return summary(db)
