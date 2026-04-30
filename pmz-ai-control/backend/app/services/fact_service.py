from sqlalchemy.orm import Session

from app.models.production_fact import ProductionFact


def list_rows(db: Session, period: str | None = None, limit: int = 100) -> list[ProductionFact]:
    q = db.query(ProductionFact)
    if period:
        q = q.filter(ProductionFact.fact_period == period)
    return q.order_by(ProductionFact.id.desc()).limit(limit).all()


def create_row(
    db: Session,
    fact_period: str,
    order_number: str,
    material_code: str | None,
    work_center: str | None,
    fact_qty: float,
    fact_hours: float,
) -> ProductionFact:
    row = ProductionFact(
        fact_period=fact_period,
        order_number=order_number,
        material_code=material_code,
        work_center=work_center,
        fact_qty=fact_qty,
        fact_hours=fact_hours,
    )
    db.add(row)
    db.commit()
    db.refresh(row)
    return row
