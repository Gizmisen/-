from sqlalchemy.orm import Session

from app.models.orders import Order
from app.models.production_fact import ProductionFact
from app.models.production_plan import ProductionPlan


def find_order(db: Session, order_number: str) -> dict | None:
    order = db.query(Order).filter(Order.order_number == order_number).first()
    if not order:
        return None
    return {
        "order_number": order.order_number,
        "status": order.status,
        "plant": order.plant,
        "quantity": float(order.quantity or 0),
    }


def find_material_usage(db: Session, material_code: str) -> dict:
    plan_count = db.query(ProductionPlan).filter(ProductionPlan.material_code == material_code).count()
    fact_count = db.query(ProductionFact).filter(ProductionFact.material_code == material_code).count()
    return {"material_code": material_code, "plan_rows": plan_count, "fact_rows": fact_count}


def analyze_plan_fact(db: Session, period: str | None = None) -> list[dict]:
    query = db.query(ProductionPlan)
    if period:
        query = query.filter(ProductionPlan.plan_period == period)

    issues = []
    for p in query.all():
        fact = (
            db.query(ProductionFact)
            .filter(
                ProductionFact.order_number == p.order_number,
                ProductionFact.material_code == p.material_code,
                ProductionFact.department == p.department,
            )
            .first()
        )
        fact_qty = float(fact.fact_qty) if fact and fact.fact_qty else 0.0
        plan_qty = float(p.planned_qty or 0)
        if plan_qty > fact_qty:
            issues.append(
                {
                    "order_number": p.order_number,
                    "material_code": p.material_code,
                    "department": p.department,
                    "plan_qty": plan_qty,
                    "fact_qty": fact_qty,
                    "gap": plan_qty - fact_qty,
                }
            )
    return issues


def answer_query(db: Session, query: str) -> tuple[str, dict | list | None]:
    q = query.lower()
    if "заказ" in q:
        number = "".join(ch for ch in query if ch.isdigit())
        if number:
            data = find_order(db, number)
            if data:
                return f"Заказ {number} найден. Статус: {data.get('status') or 'не указан'}.", data
            return f"Заказ {number} не найден.", None

    if "материал" in q:
        token = query.strip().split()[-1]
        data = find_material_usage(db, token)
        return f"Материал {token}: плановых строк {data['plan_rows']}, фактических строк {data['fact_rows']}.", data

    if "план" in q and "факт" in q:
        period = None
        for part in query.split():
            if len(part) == 7 and part[4] == "-":
                period = part
                break
        issues = analyze_plan_fact(db, period=period)
        return f"Найдено {len(issues)} позиций с недовыполнением.", issues[:50]

    return (
        "Я умею: искать заказ, анализировать план-факт, проверять материал. "
        "Пример: 'Что не закрыто по заказу 102100118179?'",
        None,
    )
