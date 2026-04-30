from datetime import date

from sqlalchemy.orm import Session

from app.models.orders import Order


def list_rows(db: Session, limit: int = 100) -> list[Order]:
    return db.query(Order).order_by(Order.id.desc()).limit(limit).all()


def create_row(db: Session, order_number: str, plant: str | None, quantity: float, required_date: date | None, status: str | None) -> Order:
    row = Order(order_number=order_number, plant=plant, quantity=quantity, required_date=required_date, status=status)
    db.add(row)
    db.commit()
    db.refresh(row)
    return row
