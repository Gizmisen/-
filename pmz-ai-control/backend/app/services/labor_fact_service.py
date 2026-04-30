from sqlalchemy.orm import Session

from app.models.extended_contour import LaborFact


def list_rows(db: Session, period: str | None = None, limit: int = 100) -> list[LaborFact]:
    q = db.query(LaborFact)
    if period:
        q = q.filter(LaborFact.period == period)
    return q.order_by(LaborFact.id.desc()).limit(limit).all()


def create_row(db: Session, period: str, order_number: str, work_center: str | None, labor_hours: float) -> LaborFact:
    row = LaborFact(period=period, order_number=order_number, work_center=work_center, labor_hours=labor_hours)
    db.add(row)
    db.commit()
    db.refresh(row)
    return row
