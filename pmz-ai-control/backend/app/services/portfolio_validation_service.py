from collections import Counter
import re

from sqlalchemy.orm import Session

from app.models.extended_contour import OrderPortfolio
from app.models.materials import Material


def find_duplicates(db: Session) -> list[dict]:
    rows = db.query(OrderPortfolio).all()
    keys = [
        (r.plant or "", r.customer_name or "", r.planning_variant or "", r.order_number or "", r.material_code or "", r.period or "")
        for r in rows
    ]
    c = Counter(keys)
    return [
        {
            "plant": k[0],
            "customer_name": k[1],
            "planning_variant": k[2],
            "order_number": k[3],
            "material_code": k[4],
            "period": k[5],
            "count": n,
        }
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


def find_missing_required_fields(db: Session) -> list[dict]:
    out: list[dict] = []
    for r in db.query(OrderPortfolio).all():
        missing = []
        if not (r.plant or "").strip():
            missing.append("plant")
        if not (r.customer_name or "").strip():
            missing.append("customer_name")
        if not (r.planning_variant or "").strip():
            missing.append("planning_variant")
        if not (r.material_code or "").strip():
            missing.append("material_code")
        if not (r.material_name or "").strip():
            missing.append("material_name")
        if r.qty is None:
            missing.append("variant_qty")
        if r.planned_delivery_date is None:
            missing.append("variant_delivery_date")
        if not (r.order_status or "").strip():
            missing.append("order_status")
        if missing:
            out.append({"portfolio_id": r.id, "order_number": r.order_number, "missing_fields": missing})
    return out


def _normalize_order_number(order_number: str | None) -> str:
    raw = (order_number or "").strip()
    digits = re.sub(r"\D", "", raw)
    if digits.startswith("55") and len(digits) > 2:
        return digits[2:]
    return digits or raw


def find_duplicates_smart(db: Session) -> list[dict]:
    rows = db.query(OrderPortfolio).all()
    full = Counter()
    soft = Counter()

    for r in rows:
        full_key = (r.plant or "", r.customer_name or "", r.planning_variant or "", r.order_number or "", r.material_code or "", r.period or "")
        full[full_key] += 1

        normalized_order = _normalize_order_number(r.order_number)
        soft_key = (r.plant or "", r.material_code or "", normalized_order, r.period or "")
        soft[soft_key] += 1

    out: list[dict] = []
    for k, n in full.items():
        if n > 1:
            out.append({"duplicate_type": "exact_full_key", "count": n, "plant": k[0], "customer_name": k[1], "planning_variant": k[2], "order_number": k[3], "material_code": k[4], "period": k[5]})
    for k, n in soft.items():
        if n > 1:
            out.append({"duplicate_type": "normalized_order_match", "count": n, "plant": k[0], "material_code": k[1], "normalized_order_number": k[2], "period": k[3]})
    return out
