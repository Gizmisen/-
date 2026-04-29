from sqlalchemy import Date, DateTime, ForeignKey, Numeric, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True)
    order_number: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)
    customer_order: Mapped[str | None] = mapped_column(String(64))
    customer_id: Mapped[int | None] = mapped_column(nullable=True)
    material_id: Mapped[int | None] = mapped_column(ForeignKey("materials.id"))
    plant: Mapped[str | None] = mapped_column(String(32))
    quantity: Mapped[float | None] = mapped_column(Numeric(18, 6))
    unit: Mapped[str | None] = mapped_column(String(32))
    contract_number: Mapped[str | None] = mapped_column(String(128))
    required_date: Mapped[str | None] = mapped_column(Date)
    status: Mapped[str | None] = mapped_column(String(32))
    source_file_id: Mapped[int | None] = mapped_column(nullable=True)
    created_at: Mapped[str] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[str] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
