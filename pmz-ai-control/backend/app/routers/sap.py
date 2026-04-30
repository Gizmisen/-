from datetime import date

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database import get_db
from app.services.sap_service import create_date, create_order, summary

router = APIRouter(prefix="/sap", tags=["sap"])


class SapOrderCreate(BaseModel):
    sap_order: str
    order_number: str | None = None
    status: str | None = None


class SapDateCreate(BaseModel):
    sap_order: str
    date_type: str
    value_date: date | None = None


@router.get("/health")
def health():
    return {"module": "sap", "status": "ready"}


@router.get("/summary")
def sap_summary(db: Session = Depends(get_db)):
    return summary(db)


@router.post("/orders")
def add_order(payload: SapOrderCreate, db: Session = Depends(get_db)):
    x = create_order(db, sap_order=payload.sap_order, order_number=payload.order_number, status=payload.status)
    return {"id": x.id}


@router.post("/dates")
def add_date(payload: SapDateCreate, db: Session = Depends(get_db)):
    x = create_date(db, sap_order=payload.sap_order, date_type=payload.date_type, value_date=payload.value_date)
    return {"id": x.id}
