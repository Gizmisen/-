from sqlalchemy.orm import Session

from app.models.extended_contour import OrdersHistory


def list_rows(db: Session, order_number: str | None = None, limit: int = 100) -> list[OrdersHistory]:
    q = db.query(OrdersHistory)
    if order_number:
        q = q.filter(OrdersHistory.order_number == order_number)
    return q.order_by(OrdersHistory.id.desc()).limit(limit).all()


def create_row(db: Session, order_number: str, status: str | None, comment: str | None) -> OrdersHistory:
    row = OrdersHistory(order_number=order_number, status=status, comment=comment)
    db.add(row)
    db.commit()
    db.refresh(row)
    return row
