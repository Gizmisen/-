from sqlalchemy.orm import Session

from app.models.orders import Order


def list_rows(db: Session, limit: int = 100) -> list[Order]:
    return db.query(Order).order_by(Order.id.desc()).limit(limit).all()
