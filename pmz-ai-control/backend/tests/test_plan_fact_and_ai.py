from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base
from app.models.imports import FileImport
from app.models.production_fact import ProductionFact
from app.models.production_plan import ProductionPlan
from app.services.ai_service import answer_query
from app.services.import_service import validate_columns
from app.services.plan_fact_service import build_plan_fact_report


def make_db():
    engine = create_engine("sqlite+pysqlite:///:memory:", future=True)
    Base.metadata.create_all(bind=engine)
    return sessionmaker(bind=engine, future=True)


def test_plan_fact_statuses_and_ai_query():
    Session = make_db()
    with Session() as db:
        db.add_all([
            ProductionPlan(plan_period="2026-03", plan_version="BP", order_number="102", material_code="MAT-1", plant="1420", department="UMK", work_center="WC1", planned_qty=100, planned_hours=10),
            ProductionFact(fact_period="2026-03", order_number="102", material_code="MAT-1", plant="1420", department="UMK", work_center="WC1", fact_qty=60, fact_hours=6),
            ProductionFact(fact_period="2026-03", order_number="999", material_code="MAT-X", plant="1420", department="UMK", work_center="WC1", fact_qty=10, fact_hours=2),
        ])
        db.commit()

        report = build_plan_fact_report(db, "2026-03")
        statuses = {r["status"] for r in report}
        assert "в работе" in statuses
        assert "вне плана" in statuses

        answer, data, mode = answer_query(db, "Покажи план факт 2026-03", advanced=False)
        assert "Найдено" in answer
        assert isinstance(data, list)
        assert mode == "local"


def test_validate_columns_and_missing_required():
    missing = validate_columns({"a", "b"}, {"a", "c"})
    assert missing == ["c"]


def test_plan_equals_fact_status_done():
    Session = make_db()
    with Session() as db:
        db.add(ProductionPlan(plan_period="2026-03", plan_version="BP", order_number="1", material_code="M", plant="1420", department="D", work_center="W", planned_qty=50, planned_hours=5))
        db.add(ProductionFact(fact_period="2026-03", order_number="1", material_code="M", plant="1420", department="D", work_center="W", fact_qty=50, fact_hours=5))
        db.commit()
        report = build_plan_fact_report(db, "2026-03")
        assert any(r["status"] == "выполнено" for r in report)
