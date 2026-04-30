from sqlalchemy.orm import Session

from app.models.extended_contour import OrderPortfolio


def list_rows(db: Session, limit: int = 100) -> list[OrderPortfolio]:
    return db.query(OrderPortfolio).order_by(OrderPortfolio.id.desc()).limit(limit).all()


def create_row(db: Session, period: str, order_number: str, material_code: str | None, plant: str | None, qty: float) -> OrderPortfolio:
    row = OrderPortfolio(period=period, order_number=order_number, material_code=material_code, plant=plant, qty=qty)
    db.add(row)
    db.commit()
    db.refresh(row)
    return row
