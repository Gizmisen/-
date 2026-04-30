from sqlalchemy.orm import Session

from app.models.extended_contour import OrderPortfolio, OrdersHistory


def find_analogs(db: Session, material_code: str | None = None, plant: str | None = None, limit: int = 100) -> list[dict]:
    q = db.query(OrdersHistory)
    if material_code:
        q = q.filter(OrdersHistory.comment.contains(material_code) | OrdersHistory.order_number.contains(material_code))
    rows = q.limit(limit).all()
    return [{"id": r.id, "order_number": r.order_number, "status": r.status, "comment": r.comment} for r in rows]


def compare_with_portfolio(db: Session, limit: int = 200) -> list[dict]:
    history_orders = {h.order_number for h in db.query(OrdersHistory).all() if h.order_number}
    out = []
    for p in db.query(OrderPortfolio).all():
        if p.order_number not in history_orders:
            out.append({"portfolio_id": p.id, "order_number": p.order_number, "material_code": p.material_code, "plant": p.plant})
            if len(out) >= limit:
                break
    return out
