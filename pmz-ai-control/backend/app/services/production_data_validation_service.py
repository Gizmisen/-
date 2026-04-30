from collections import Counter

from sqlalchemy.orm import Session

from app.models.extended_contour import RoutingOperation
from app.models.materials import Material


def material_duplicates_by_plant(db: Session) -> list[dict]:
    rows = db.query(Material).all()
    keys = [(r.material_code, r.plant or "") for r in rows]
    c = Counter(keys)
    return [{"material_code": k[0], "plant": k[1], "count": n} for k, n in c.items() if n > 1]


def materials_without_routings(db: Session) -> list[dict]:
    routings = {(r.material_code, r.plant or "") for r in db.query(RoutingOperation).all()}
    out = []
    for m in db.query(Material).all():
        if (m.material_code, m.plant or "") not in routings:
            out.append({"material_code": m.material_code, "material_name": m.material_name, "plant": m.plant})
    return out


def material_routings(db: Session, material_code: str) -> list[dict]:
    rows = db.query(RoutingOperation).filter(RoutingOperation.material_code == material_code).all()
    return [{"id": r.id, "plant": r.plant, "work_center": r.work_center, "labor_value": float(r.labor_value or 0), "labor_unit": r.labor_unit} for r in rows]
