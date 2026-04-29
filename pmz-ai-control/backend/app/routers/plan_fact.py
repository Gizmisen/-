from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.services.plan_fact_service import build_plan_fact_report

router = APIRouter(prefix="/plan-fact", tags=["plan-fact"])


@router.get("")
def get_plan_fact(period: str | None = Query(default=None), db: Session = Depends(get_db)):
    return {"items": build_plan_fact_report(db, period=period)}
