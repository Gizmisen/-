from sqlalchemy.orm import Session

from app.models.extended_contour import LaborFact, OrderPortfolio, SapOrder, WarehouseStock
from app.models.orders import Order
from app.models.production_fact import ProductionFact
from app.models.production_plan import ProductionPlan


def build_dashboard(db: Session) -> dict:
    return {
        "portfolio_rows": db.query(OrderPortfolio).count(),
        "planning_rows": db.query(ProductionPlan).count(),
        "fact_rows": db.query(ProductionFact).count(),
        "labor_fact_rows": db.query(LaborFact).count(),
        "sales_orders": db.query(Order).count(),
        "warehouse_rows": db.query(WarehouseStock).count(),
        "sap_orders": db.query(SapOrder).count(),
    }
