from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.extended_contour import OrderPortfolio, WarehouseStock
from app.models.production_fact import ProductionFact
from app.models.production_plan import ProductionPlan


def find_plan_without_fact(db: Session, period: str | None = None, limit: int = 200) -> list[dict]:
    plan = db.query(ProductionPlan)
    fact = db.query(ProductionFact)
    if period:
        plan = plan.filter(ProductionPlan.plan_period == period)
        fact = fact.filter(ProductionFact.fact_period == period)
    fact_keys = {(x.order_number, x.material_code, x.plant, x.work_center) for x in fact.all()}
    out = []
    for p in plan.all():
        key = (p.order_number, p.material_code, p.plant, p.work_center)
        if key not in fact_keys:
            out.append({"order_number": p.order_number, "material_code": p.material_code, "plant": p.plant, "work_center": p.work_center, "period": p.plan_period})
            if len(out) >= limit:
                break
    return out


def find_fact_without_plan(db: Session, period: str | None = None, limit: int = 200) -> list[dict]:
    plan = db.query(ProductionPlan)
    fact = db.query(ProductionFact)
    if period:
        plan = plan.filter(ProductionPlan.plan_period == period)
        fact = fact.filter(ProductionFact.fact_period == period)
    plan_keys = {(x.order_number, x.material_code, x.plant, x.work_center) for x in plan.all()}
    out = []
    for f in fact.all():
        key = (f.order_number, f.material_code, f.plant, f.work_center)
        if key not in plan_keys:
            out.append({"order_number": f.order_number, "material_code": f.material_code, "plant": f.plant, "work_center": f.work_center, "period": f.fact_period})
            if len(out) >= limit:
                break
    return out


def find_portfolio_without_plan(db: Session, limit: int = 200) -> list[dict]:
    plan_keys = {(x.order_number, x.material_code, x.plant) for x in db.query(ProductionPlan).all()}
    out = []
    for p in db.query(OrderPortfolio).all():
        key = (p.order_number, p.material_code, p.plant)
        if key not in plan_keys:
            out.append({"order_number": p.order_number, "material_code": p.material_code, "plant": p.plant, "period": p.period})
            if len(out) >= limit:
                break
    return out


def find_warehouse_shortages(db: Session, limit: int = 200) -> list[dict]:
    demand = db.query(ProductionPlan.material_code, ProductionPlan.plant, func.sum(ProductionPlan.planned_qty)).group_by(ProductionPlan.material_code, ProductionPlan.plant).all()
    stock_map = {(x.material_code, x.plant): float(x.qty or 0) for x in db.query(WarehouseStock).all()}
    out = []
    for material_code, plant, total in demand:
        need = float(total or 0)
        stock = stock_map.get((material_code, plant), 0)
        if stock < need:
            out.append({"material_code": material_code, "plant": plant, "need": need, "stock": stock, "shortage": need - stock})
            if len(out) >= limit:
                break
    return out
