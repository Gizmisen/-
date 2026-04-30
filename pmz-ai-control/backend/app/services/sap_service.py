from sqlalchemy.orm import Session

from app.models.extended_contour import SapDate, SapOrder


def summary(db: Session) -> dict:
    return {"sap_orders": db.query(SapOrder).count(), "sap_dates": db.query(SapDate).count()}
