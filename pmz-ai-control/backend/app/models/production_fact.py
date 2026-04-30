from sqlalchemy import Date, DateTime, Numeric, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class ProductionFact(Base):
    __tablename__ = "production_fact"

    id: Mapped[int] = mapped_column(primary_key=True)
    fact_period: Mapped[str] = mapped_column(String(7), nullable=False)
    order_number: Mapped[str] = mapped_column(String(64), nullable=False)
    customer_order: Mapped[str | None] = mapped_column(String(64))
    material_code: Mapped[str | None] = mapped_column(String(64))
    material_name: Mapped[str | None] = mapped_column(Text())
    plant: Mapped[str | None] = mapped_column(String(32))
    department: Mapped[str | None] = mapped_column(String(64))
    work_center: Mapped[str | None] = mapped_column(String(64))
    order_qty: Mapped[float | None] = mapped_column(Numeric(18, 6))
    delivered_qty: Mapped[float | None] = mapped_column(Numeric(18, 6))
    confirmed_qty: Mapped[float | None] = mapped_column(Numeric(18, 6))
    fact_qty: Mapped[float | None] = mapped_column(Numeric(18, 6))
    fact_hours: Mapped[float | None] = mapped_column(Numeric(18, 6))
    start_date: Mapped[str | None] = mapped_column(Date)
    finish_date: Mapped[str | None] = mapped_column(Date)
    system_status: Mapped[str | None] = mapped_column(String(128))
    sap_order: Mapped[str | None] = mapped_column(String(64))
    source_file_id: Mapped[int | None] = mapped_column(nullable=True)
    imported_at: Mapped[str] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
