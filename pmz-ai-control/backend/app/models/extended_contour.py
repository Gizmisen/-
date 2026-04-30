from sqlalchemy import Date, DateTime, Numeric, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class OrderPortfolio(Base):
    __tablename__ = "order_portfolio"
    id: Mapped[int] = mapped_column(primary_key=True)
    period: Mapped[str] = mapped_column(String(7), nullable=False)
    order_number: Mapped[str] = mapped_column(String(64), nullable=False)
    material_code: Mapped[str | None] = mapped_column(String(64))
    material_name: Mapped[str | None] = mapped_column(Text())
    plant: Mapped[str | None] = mapped_column(String(32))
    qty: Mapped[float | None] = mapped_column(Numeric(18, 6))
    created_at: Mapped[str] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)


class OrdersHistory(Base):
    __tablename__ = "orders_history"
    id: Mapped[int] = mapped_column(primary_key=True)
    order_number: Mapped[str] = mapped_column(String(64), nullable=False)
    status: Mapped[str | None] = mapped_column(String(64))
    event_date: Mapped[str | None] = mapped_column(Date)
    comment: Mapped[str | None] = mapped_column(Text())


class PlanVersion(Base):
    __tablename__ = "plan_versions"
    id: Mapped[int] = mapped_column(primary_key=True)
    period: Mapped[str] = mapped_column(String(7), nullable=False)
    version_code: Mapped[str] = mapped_column(String(32), nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True, nullable=False)
    created_at: Mapped[str] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)


class PlanVersionRow(Base):
    __tablename__ = "plan_version_rows"
    id: Mapped[int] = mapped_column(primary_key=True)
    plan_version_id: Mapped[int] = mapped_column(nullable=False)
    order_number: Mapped[str] = mapped_column(String(64), nullable=False)
    material_code: Mapped[str | None] = mapped_column(String(64))
    work_center: Mapped[str | None] = mapped_column(String(64))
    planned_qty: Mapped[float | None] = mapped_column(Numeric(18, 6))
    planned_hours: Mapped[float | None] = mapped_column(Numeric(18, 6))


class WarehouseStock(Base):
    __tablename__ = "warehouse_stock"
    id: Mapped[int] = mapped_column(primary_key=True)
    material_code: Mapped[str] = mapped_column(String(64), nullable=False)
    plant: Mapped[str | None] = mapped_column(String(32))
    qty: Mapped[float | None] = mapped_column(Numeric(18, 6))
    snapshot_date: Mapped[str | None] = mapped_column(Date)


class SapOrder(Base):
    __tablename__ = "sap_orders"
    id: Mapped[int] = mapped_column(primary_key=True)
    sap_order: Mapped[str] = mapped_column(String(64), nullable=False)
    order_number: Mapped[str | None] = mapped_column(String(64))
    status: Mapped[str | None] = mapped_column(String(64))


class SapDate(Base):
    __tablename__ = "sap_dates"
    id: Mapped[int] = mapped_column(primary_key=True)
    sap_order: Mapped[str] = mapped_column(String(64), nullable=False)
    date_type: Mapped[str] = mapped_column(String(32), nullable=False)
    value_date: Mapped[str | None] = mapped_column(Date)


class LaborFact(Base):
    __tablename__ = "labor_fact"
    id: Mapped[int] = mapped_column(primary_key=True)
    period: Mapped[str] = mapped_column(String(7), nullable=False)
    order_number: Mapped[str] = mapped_column(String(64), nullable=False)
    work_center: Mapped[str | None] = mapped_column(String(64))
    labor_hours: Mapped[float | None] = mapped_column(Numeric(18, 6))
