from collections import defaultdict

from sqlalchemy.orm import Session

from app.models.production_fact import ProductionFact
from app.models.production_plan import ProductionPlan


def build_plan_fact_report(db: Session, period: str | None = None) -> list[dict]:
    plan_q = db.query(ProductionPlan)
    fact_q = db.query(ProductionFact)
    if period:
        plan_q = plan_q.filter(ProductionPlan.plan_period == period)
        fact_q = fact_q.filter(ProductionFact.fact_period == period)

    rows = defaultdict(
        lambda: {
            "plan_qty": 0.0,
            "plan_hours": 0.0,
            "fact_qty": 0.0,
            "fact_hours": 0.0,
            "plan_version": None,
            "period": period,
        }
    )

    for p in plan_q.all():
        key = (p.order_number, p.material_code, p.plant, p.department, p.work_center, p.plan_period, p.plan_version)
        rows[key].update({"order_number": p.order_number, "material_code": p.material_code, "plant": p.plant, "department": p.department, "work_center": p.work_center, "plan_version": p.plan_version, "period": p.plan_period})
        rows[key]["plan_qty"] += float(p.planned_qty or 0)
        rows[key]["plan_hours"] += float(p.planned_hours or 0)

    for f in fact_q.all():
        key = (f.order_number, f.material_code, f.plant, f.department, f.work_center, f.fact_period, None)
        rows[key].update({"order_number": f.order_number, "material_code": f.material_code, "plant": f.plant, "department": f.department, "work_center": f.work_center, "period": f.fact_period})
        rows[key]["fact_qty"] += float(f.fact_qty or 0)
        rows[key]["fact_hours"] += float(f.fact_hours or 0)

    result = []
    for row in rows.values():
        plan_qty, fact_qty = row["plan_qty"], row["fact_qty"]
        plan_hours, fact_hours = row["plan_hours"], row["fact_hours"]
        status = "в работе"
        if plan_qty == 0 and fact_qty > 0:
            status = "вне плана"
        elif plan_qty > 0 and fact_qty == 0:
            status = "нет факта"
        elif plan_qty == fact_qty:
            status = "выполнено"
        elif fact_qty > plan_qty:
            status = "перевыполнение"
        result.append({**row, "remaining_qty": plan_qty - fact_qty, "remaining_hours": plan_hours - fact_hours, "completion_percent": (fact_qty / plan_qty * 100) if plan_qty else 0, "status": status})
    return result
