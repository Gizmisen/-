from sqlalchemy import Date, DateTime, Numeric, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class ProductionPlan(Base):
    __tablename__ = "production_plan"

    id: Mapped[int] = mapped_column(primary_key=True)
    plan_period: Mapped[str] = mapped_column(String(7), nullable=False)
    plan_version: Mapped[str] = mapped_column(String(32), nullable=False)
    order_number: Mapped[str] = mapped_column(String(64), nullable=False)
    material_code: Mapped[str | None] = mapped_column(String(64))
    material_name: Mapped[str | None] = mapped_column(Text())
    plant: Mapped[str | None] = mapped_column(String(32))
    department: Mapped[str | None] = mapped_column(String(64))
    work_center: Mapped[str | None] = mapped_column(String(64))
    planned_qty: Mapped[float | None] = mapped_column(Numeric(18, 6))
    planned_hours: Mapped[float | None] = mapped_column(Numeric(18, 6))
    planned_weight: Mapped[float | None] = mapped_column(Numeric(18, 6))
    plan_date: Mapped[str | None] = mapped_column(Date)
    source_file_id: Mapped[int | None] = mapped_column(nullable=True)
    created_at: Mapped[str] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
