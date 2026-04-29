from sqlalchemy import Boolean, DateTime, Numeric, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Material(Base):
    __tablename__ = "materials"

    id: Mapped[int] = mapped_column(primary_key=True)
    material_code: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)
    material_name: Mapped[str] = mapped_column(Text(), nullable=False)
    unit: Mapped[str | None] = mapped_column(String(32))
    plant: Mapped[str | None] = mapped_column(String(32))
    material_group: Mapped[str | None] = mapped_column(String(64))
    drawing_number: Mapped[str | None] = mapped_column(String(128))
    weight: Mapped[float | None] = mapped_column(Numeric(18, 6))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[str] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[str] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
