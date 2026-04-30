import csv
import io

from fastapi import APIRouter, Depends, Query
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app.database import get_db
from app.services.plan_fact_service import build_plan_fact_report

router = APIRouter(prefix="/plan-fact", tags=["plan-fact"])


@router.get("")
def get_plan_fact(
    period: str | None = Query(default=None),
    status: str | None = Query(default=None),
    limit: int = Query(default=200, ge=1, le=2000),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
):
    items = build_plan_fact_report(db, period=period)
    if status:
        items = [x for x in items if x.get("status") == status]
    total = len(items)
    return {"total": total, "items": items[offset : offset + limit]}


@router.get("/export")
def export_plan_fact(period: str | None = Query(default=None), db: Session = Depends(get_db)):
    items = build_plan_fact_report(db, period=period)
    output = io.StringIO()
    writer = csv.DictWriter(
        output,
        fieldnames=["order_number", "material_code", "department", "plan_qty", "fact_qty", "remaining_qty", "plan_hours", "fact_hours", "remaining_hours", "completion_percent", "status"],
    )
    writer.writeheader()
    for row in items:
        writer.writerow(row)
    output.seek(0)
    filename = f"plan_fact_{period or 'all'}.csv"
    return StreamingResponse(iter([output.getvalue()]), media_type="text/csv", headers={"Content-Disposition": f"attachment; filename={filename}"})
