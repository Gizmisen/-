from sqlalchemy.orm import Session

from app.models.extended_contour import PlanVersion, PlanVersionRow


def create_version(db: Session, period: str, version_code: str, is_active: bool = True) -> PlanVersion:
    row = PlanVersion(period=period, version_code=version_code, is_active=is_active)
    db.add(row)
    db.commit()
    db.refresh(row)
    return row


def add_row(db: Session, plan_version_id: int, order_number: str, material_code: str | None, work_center: str | None, planned_qty: float, planned_hours: float) -> PlanVersionRow:
    row = PlanVersionRow(plan_version_id=plan_version_id, order_number=order_number, material_code=material_code, work_center=work_center, planned_qty=planned_qty, planned_hours=planned_hours)
    db.add(row)
    db.commit()
    db.refresh(row)
    return row


def compare_versions(db: Session, left_version_id: int, right_version_id: int) -> dict:
    left = db.query(PlanVersionRow).filter(PlanVersionRow.plan_version_id == left_version_id).all()
    right = db.query(PlanVersionRow).filter(PlanVersionRow.plan_version_id == right_version_id).all()
    lmap = {(x.order_number, x.material_code, x.work_center): x for x in left}
    rmap = {(x.order_number, x.material_code, x.work_center): x for x in right}
    added = [k for k in rmap if k not in lmap]
    removed = [k for k in lmap if k not in rmap]
    changed = []
    for k in set(lmap).intersection(rmap):
        lq, rq = float(lmap[k].planned_qty or 0), float(rmap[k].planned_qty or 0)
        lh, rh = float(lmap[k].planned_hours or 0), float(rmap[k].planned_hours or 0)
        if lq != rq or lh != rh:
            changed.append({"key": k, "qty_delta": rq - lq, "hours_delta": rh - lh})
    return {"added": added, "removed": removed, "changed": changed}
