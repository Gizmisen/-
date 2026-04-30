from datetime import date

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.extended_contour import OrderPortfolio


def list_rows(
    db: Session,
    limit: int = 100,
    offset: int = 0,
    material_code: str | None = None,
    order_number: str | None = None,
    plant: str | None = None,
    period: str | None = None,
    order_status: str | None = None,
) -> list[OrderPortfolio]:
    query = db.query(OrderPortfolio)
    if material_code:
        query = query.filter(OrderPortfolio.material_code == material_code)
    if order_number:
        query = query.filter(OrderPortfolio.order_number == order_number)
    if plant:
        query = query.filter(OrderPortfolio.plant == plant)
    if period:
        query = query.filter(OrderPortfolio.period == period)
    if order_status:
        query = query.filter(OrderPortfolio.order_status == order_status)
    return query.order_by(OrderPortfolio.id.desc()).offset(offset).limit(limit).all()


def count_rows(db: Session) -> int:
    return db.query(func.count(OrderPortfolio.id)).scalar() or 0


def get_row(db: Session, row_id: int) -> OrderPortfolio | None:
    return db.query(OrderPortfolio).filter(OrderPortfolio.id == row_id).first()


def create_row(
    db: Session,
    period: str,
    order_number: str,
    material_code: str | None,
    plant: str | None,
    qty: float,
    customer_name: str | None = None,
    planning_variant: str | None = None,
    note: str | None = None,
    planned_delivery_date: date | None = None,
) -> OrderPortfolio:
    row = OrderPortfolio(
        period=period,
        order_number=order_number,
        material_code=material_code,
        plant=plant,
        qty=qty,
        customer_name=customer_name,
        planning_variant=planning_variant,
        note=note,
        planned_delivery_date=planned_delivery_date,
    )
    db.add(row)
    db.commit()
    db.refresh(row)
    return row


def update_row(db: Session, row_id: int, payload: dict) -> OrderPortfolio | None:
    row = get_row(db, row_id)
    if not row:
        return None
    for field in ["qty", "note", "planned_delivery_date", "planning_variant", "order_status"]:
        if field in payload:
            setattr(row, field, payload[field])
    db.commit()
    db.refresh(row)
    return row
