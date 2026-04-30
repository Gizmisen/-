from sqlalchemy.orm import Session

from app.models.production_plan import ProductionPlan


def list_rows(db: Session, period: str | None = None, limit: int = 100) -> list[ProductionPlan]:
    q = db.query(ProductionPlan)
    if period:
        q = q.filter(ProductionPlan.plan_period == period)
    return q.order_by(ProductionPlan.id.desc()).limit(limit).all()
