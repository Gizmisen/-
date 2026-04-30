from sqlalchemy.orm import Session

from app.models.production_plan import ProductionPlan


def list_rows(db: Session, period: str | None = None, limit: int = 100) -> list[ProductionPlan]:
    q = db.query(ProductionPlan)
    if period:
        q = q.filter(ProductionPlan.plan_period == period)
    return q.order_by(ProductionPlan.id.desc()).limit(limit).all()


def create_row(
    db: Session,
    plan_period: str,
    plan_version: str,
    order_number: str,
    material_code: str | None,
    work_center: str | None,
    planned_qty: float,
    planned_hours: float,
) -> ProductionPlan:
    row = ProductionPlan(
        plan_period=plan_period,
        plan_version=plan_version,
        order_number=order_number,
        material_code=material_code,
        work_center=work_center,
        planned_qty=planned_qty,
        planned_hours=planned_hours,
    )
    db.add(row)
    db.commit()
    db.refresh(row)
    return row
