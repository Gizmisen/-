from sqlalchemy.orm import Session

from app.models.extended_contour import OrderPortfolio


def list_rows(db: Session, limit: int = 100) -> list[OrderPortfolio]:
    return db.query(OrderPortfolio).order_by(OrderPortfolio.id.desc()).limit(limit).all()
