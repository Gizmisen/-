from datetime import date

from sqlalchemy.orm import Session

from app.models.orders import Order


def list_orders(
    db: Session,
    limit: int = 100,
    offset: int = 0,
    status: str | None = None,
    plant: str | None = None,
) -> list[Order]:
    query = db.query(Order)
    if status:
        query = query.filter(Order.status == status)
    if plant:
        query = query.filter(Order.plant == plant)
    return query.order_by(Order.id.desc()).offset(offset).limit(limit).all()


def get_order(db: Session, order_number: str) -> Order | None:
    return db.query(Order).filter(Order.order_number == order_number).first()


def create_order(
    db: Session,
    order_number: str,
    customer_order: str | None = None,
    plant: str | None = None,
    quantity: float | None = None,
    unit: str | None = None,
    contract_number: str | None = None,
    required_date: date | None = None,
    status: str | None = None,
) -> Order:
    existing = get_order(db, order_number)
    if existing:
        return existing
    row = Order(
        order_number=order_number,
        customer_order=customer_order,
        plant=plant,
        quantity=quantity,
        unit=unit,
        contract_number=contract_number,
        required_date=required_date,
        status=status,
    )
    db.add(row)
    db.commit()
    db.refresh(row)
    return row


def update_order(db: Session, order_number: str, payload: dict) -> Order | None:
    row = get_order(db, order_number)
    if not row:
        return None
    for field in ["customer_order", "plant", "quantity", "unit", "contract_number", "required_date", "status"]:
        if field in payload:
            setattr(row, field, payload[field])
    db.commit()
    db.refresh(row)
    return row
