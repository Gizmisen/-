from datetime import date

from sqlalchemy.orm import Session

from app.models.extended_contour import WarehouseStock


def list_rows(db: Session, limit: int = 100) -> list[WarehouseStock]:
    return db.query(WarehouseStock).order_by(WarehouseStock.id.desc()).limit(limit).all()


def create_row(db: Session, material_code: str, plant: str | None, qty: float, snapshot_date: date | None) -> WarehouseStock:
    row = WarehouseStock(material_code=material_code, plant=plant, qty=qty, snapshot_date=snapshot_date)
    db.add(row)
    db.commit()
    db.refresh(row)
    return row
