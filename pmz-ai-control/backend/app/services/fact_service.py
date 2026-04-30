from sqlalchemy.orm import Session

from app.models.production_fact import ProductionFact


def list_rows(db: Session, period: str | None = None, limit: int = 100) -> list[ProductionFact]:
    q = db.query(ProductionFact)
    if period:
        q = q.filter(ProductionFact.fact_period == period)
    return q.order_by(ProductionFact.id.desc()).limit(limit).all()
