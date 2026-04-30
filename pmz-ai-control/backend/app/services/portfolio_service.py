from datetime import date

from sqlalchemy.orm import Session

from app.models.extended_contour import OrderPortfolio


def list_rows(db: Session, limit: int = 100) -> list[OrderPortfolio]:
    return db.query(OrderPortfolio).order_by(OrderPortfolio.id.desc()).limit(limit).all()


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
