from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base
from app.models.production_fact import ProductionFact
from app.models.production_plan import ProductionPlan
from app.services.ai_service import answer_query
from app.services.plan_fact_service import build_plan_fact_report


def test_plan_fact_and_ai_query():
    engine = create_engine("sqlite+pysqlite:///:memory:", future=True)
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine, future=True)

    with Session() as db:
        db.add(ProductionPlan(plan_period="2026-03", plan_version="BP", order_number="102", material_code="MAT-1", department="UMK", planned_qty=100, planned_hours=10))
        db.add(ProductionFact(fact_period="2026-03", order_number="102", material_code="MAT-1", department="UMK", fact_qty=60, fact_hours=6))
        db.commit()

        report = build_plan_fact_report(db, "2026-03")
        assert len(report) == 1
        assert report[0]["remaining_qty"] == 40
        assert report[0]["status"] == "в работе"

        answer, data = answer_query(db, "Покажи план факт 2026-03")
        assert "Найдено" in answer
        assert isinstance(data, list)
