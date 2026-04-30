from sqlalchemy.orm import Session

from app.models.materials import Material


def get_summary(db: Session) -> dict:
    return {"materials": db.query(Material).count()}


def list_materials(db: Session, limit: int = 100) -> list[Material]:
    return db.query(Material).order_by(Material.id.desc()).limit(limit).all()


def create_material(db: Session, material_code: str, material_name: str, unit: str | None, plant: str | None) -> Material:
    row = Material(material_code=material_code, material_name=material_name, unit=unit, plant=plant)
    db.add(row)
    db.commit()
    db.refresh(row)
    return row
