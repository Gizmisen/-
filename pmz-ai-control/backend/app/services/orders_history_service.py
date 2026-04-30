from sqlalchemy.orm import Session

from app.models.extended_contour import OrdersHistory


def list_rows(
    db: Session,
    order_number: str | None = None,
    material_code: str | None = None,
    customer_name: str | None = None,
    limit: int = 100,
) -> list[OrdersHistory]:
    q = db.query(OrdersHistory)
    if order_number:
        q = q.filter(OrdersHistory.order_number == order_number)
    if material_code:
        q = q.filter(OrdersHistory.material_code == material_code)
    if customer_name:
        q = q.filter(OrdersHistory.customer_name == customer_name)
    return q.order_by(OrdersHistory.id.desc()).limit(limit).all()


def create_row(db: Session, order_number: str, status: str | None, comment: str | None) -> OrdersHistory:
    row = OrdersHistory(order_number=order_number, status=status, comment=comment)
    db.add(row)
    db.commit()
    db.refresh(row)
    return row


def get_row(db: Session, row_id: int) -> OrdersHistory | None:
    return db.query(OrdersHistory).filter(OrdersHistory.id == row_id).first()
