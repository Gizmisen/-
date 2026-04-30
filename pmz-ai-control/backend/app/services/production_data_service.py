from sqlalchemy.orm import Session

from app.models.extended_contour import BomSpec, RoutingOperation
from app.models.materials import Material


def get_summary(db: Session) -> dict:
    return {
        "materials": db.query(Material).count(),
        "bom_specs": db.query(BomSpec).count(),
        "routings": db.query(RoutingOperation).count(),
    }


def list_materials(db: Session, limit: int = 100) -> list[Material]:
    return db.query(Material).order_by(Material.id.desc()).limit(limit).all()


def find_material(db: Session, material_code: str, plant: str | None = None) -> Material | None:
    query = db.query(Material).filter(Material.material_code == material_code)
    if plant is not None:
        query = query.filter(Material.plant == plant)
    return query.first()


def create_material(db: Session, material_code: str, material_name: str, unit: str | None, plant: str | None) -> Material:
    exists = find_material(db, material_code=material_code, plant=plant)
    if exists:
        exists.material_name = material_name
        exists.unit = unit
        db.commit()
        db.refresh(exists)
        return exists
    row = Material(material_code=material_code, material_name=material_name, unit=unit, plant=plant)
    db.add(row)
    db.commit()
    db.refresh(row)
    return row


def list_specs(db: Session, limit: int = 100) -> list[BomSpec]:
    return db.query(BomSpec).order_by(BomSpec.id.desc()).limit(limit).all()


def create_spec(db: Session, parent_material_code: str, plant: str | None, component_code: str, component_qty: float, component_unit: str | None) -> BomSpec:
    row = BomSpec(parent_material_code=parent_material_code, plant=plant, component_code=component_code, component_qty=component_qty, component_unit=component_unit)
    db.add(row)
    db.commit()
    db.refresh(row)
    return row


def list_routings(db: Session, limit: int = 100) -> list[RoutingOperation]:
    return db.query(RoutingOperation).order_by(RoutingOperation.id.desc()).limit(limit).all()


def create_routing(db: Session, material_code: str, plant: str | None, work_center: str, labor_value: float, labor_unit: str | None) -> RoutingOperation:
    row = RoutingOperation(material_code=material_code, plant=plant, work_center=work_center, labor_value=labor_value, labor_unit=labor_unit or "h")
    db.add(row)
    db.commit()
    db.refresh(row)
    return row
