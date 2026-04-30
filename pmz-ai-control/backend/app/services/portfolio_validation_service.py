from collections import Counter

from sqlalchemy.orm import Session

from app.models.extended_contour import OrderPortfolio
from app.models.materials import Material


def find_duplicates(db: Session) -> list[dict]:
    rows = db.query(OrderPortfolio).all()
    keys = [(r.plant or "", r.order_number or "", r.material_code or "", r.period or "") for r in rows]
    c = Counter(keys)
    return [
        {"plant": k[0], "order_number": k[1], "material_code": k[2], "period": k[3], "count": n}
        for k, n in c.items()
        if n > 1
    ]


def find_missing_materials(db: Session) -> list[dict]:
    mats = {(m.material_code, m.plant or "") for m in db.query(Material).all()}
    out = []
    for r in db.query(OrderPortfolio).all():
        key = (r.material_code or "", r.plant or "")
        if key not in mats:
            out.append({"portfolio_id": r.id, "material_code": r.material_code, "plant": r.plant, "order_number": r.order_number})
    return out
