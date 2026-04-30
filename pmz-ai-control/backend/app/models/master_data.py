from datetime import date, datetime

from sqlalchemy import Boolean, Date, DateTime, ForeignKey, Integer, Numeric, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class WorkCenter(Base):
    __tablename__ = "work_centers"
    id: Mapped[int] = mapped_column(primary_key=True)
    work_center_name: Mapped[str] = mapped_column(String(255), nullable=False)
    work_center_number: Mapped[str] = mapped_column(String(64), nullable=False)
    department: Mapped[str] = mapped_column(String(128), nullable=False)
    plant: Mapped[str] = mapped_column(String(32), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    source_file_id: Mapped[int | None] = mapped_column(nullable=True)
    source_sheet: Mapped[str | None] = mapped_column(String(255))
    source_row_number: Mapped[int | None] = mapped_column(Integer)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)


class Customer(Base):
    __tablename__ = "customers"
    id: Mapped[int] = mapped_column(primary_key=True)
    customer_code: Mapped[str | None] = mapped_column(String(64))
    customer_name: Mapped[str] = mapped_column(String(255), nullable=False)
    short_name: Mapped[str | None] = mapped_column(String(255))
    plant: Mapped[str | None] = mapped_column(String(32))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    source_file_id: Mapped[int | None] = mapped_column(nullable=True)
    source_sheet: Mapped[str | None] = mapped_column(String(255))
    source_row_number: Mapped[int | None] = mapped_column(Integer)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)


class Plant(Base):
    __tablename__ = "plants"
    id: Mapped[int] = mapped_column(primary_key=True)
    plant_code: Mapped[str] = mapped_column(String(32), unique=True, nullable=False)
    plant_name: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    source_file_id: Mapped[int | None] = mapped_column(nullable=True)
    source_sheet: Mapped[str | None] = mapped_column(String(255))
    source_row_number: Mapped[int | None] = mapped_column(Integer)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)


class PortfolioPlanningVariant(Base):
    __tablename__ = "portfolio_planning_variants"
    id: Mapped[int] = mapped_column(primary_key=True)
    variant_code: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)
    variant_name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text())
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)


class PortfolioBatchImportRow(Base):
    __tablename__ = "portfolio_batch_import_rows"
    id: Mapped[int] = mapped_column(primary_key=True)
    file_import_id: Mapped[int] = mapped_column(ForeignKey("file_imports.id"), nullable=False)
    source_sheet: Mapped[str | None] = mapped_column(String(255))
    source_row_number: Mapped[int | None] = mapped_column(Integer)
    plant: Mapped[str | None] = mapped_column(String(32))
    customer_name: Mapped[str | None] = mapped_column(String(255))
    planning_variant: Mapped[str | None] = mapped_column(String(64))
    year: Mapped[int | None] = mapped_column(Integer)
    month: Mapped[int | None] = mapped_column(Integer)
    order_number: Mapped[str | None] = mapped_column(String(64))
    order_open_date: Mapped[date | None] = mapped_column(Date)
    material_code: Mapped[str | None] = mapped_column(String(64))
    material_name: Mapped[str | None] = mapped_column(Text())
    variant_qty: Mapped[float | None] = mapped_column(Numeric(18, 6))
    delivery_date: Mapped[date | None] = mapped_column(Date)
    status: Mapped[str | None] = mapped_column(String(64))
    note: Mapped[str | None] = mapped_column(Text())
    validation_status: Mapped[str | None] = mapped_column(String(32))
    error_message: Mapped[str | None] = mapped_column(Text())
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)


class PortfolioDuplicateCheck(Base):
    __tablename__ = "portfolio_duplicate_checks"
    id: Mapped[int] = mapped_column(primary_key=True)
    plant: Mapped[str | None] = mapped_column(String(32))
    customer_name: Mapped[str | None] = mapped_column(String(255))
    planning_variant: Mapped[str | None] = mapped_column(String(64))
    order_number: Mapped[str | None] = mapped_column(String(64))
    material_code: Mapped[str | None] = mapped_column(String(64))
    period: Mapped[str | None] = mapped_column(String(7))
    duplicate_count: Mapped[int | None] = mapped_column(Integer)
    duplicate_type: Mapped[str | None] = mapped_column(String(64))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)


class OrdersHistoryLink(Base):
    __tablename__ = "orders_history_links"
    id: Mapped[int] = mapped_column(primary_key=True)
    portfolio_id: Mapped[int] = mapped_column(ForeignKey("order_portfolio.id"), nullable=False)
    history_id: Mapped[int] = mapped_column(ForeignKey("orders_history.id"), nullable=False)
    match_type: Mapped[str | None] = mapped_column(String(64))
    match_score: Mapped[float | None] = mapped_column(Numeric(5, 2))
    matched_by: Mapped[str | None] = mapped_column(String(32))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
