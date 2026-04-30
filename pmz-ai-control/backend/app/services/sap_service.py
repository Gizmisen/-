from datetime import date

from sqlalchemy.orm import Session

from app.models.extended_contour import SapDate, SapOrder


def summary(db: Session) -> dict:
    return {"sap_orders": db.query(SapOrder).count(), "sap_dates": db.query(SapDate).count()}


def create_order(db: Session, sap_order: str, order_number: str | None, status: str | None) -> SapOrder:
    row = SapOrder(sap_order=sap_order, order_number=order_number, status=status)
    db.add(row)
    db.commit()
    db.refresh(row)
    return row


def create_date(db: Session, sap_order: str, date_type: str, value_date: date | None) -> SapDate:
    row = SapDate(sap_order=sap_order, date_type=date_type, value_date=value_date)
    db.add(row)
    db.commit()
    db.refresh(row)
    return row
