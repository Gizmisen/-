from sqlalchemy.orm import Session

from app.models.extended_contour import LaborFact


def list_rows(db: Session, period: str | None = None, limit: int = 100) -> list[LaborFact]:
    q = db.query(LaborFact)
    if period:
        q = q.filter(LaborFact.period == period)
    return q.order_by(LaborFact.id.desc()).limit(limit).all()
