from sqlalchemy.orm import Session

from app.models.extended_contour import WarehouseStock


def list_rows(db: Session, limit: int = 100) -> list[WarehouseStock]:
    return db.query(WarehouseStock).order_by(WarehouseStock.id.desc()).limit(limit).all()
