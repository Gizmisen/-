from sqlalchemy import DateTime, ForeignKey, Integer, JSON, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class FileImport(Base):
    __tablename__ = "file_imports"

    id: Mapped[int] = mapped_column(primary_key=True)
    file_name: Mapped[str] = mapped_column(String(255), nullable=False)
    original_file_name: Mapped[str] = mapped_column(String(255), nullable=False)
    file_path: Mapped[str] = mapped_column(Text(), nullable=False)
    file_type: Mapped[str | None] = mapped_column(String(64))
    module: Mapped[str | None] = mapped_column(String(64))
    uploaded_by: Mapped[int | None] = mapped_column(nullable=True)
    uploaded_at: Mapped[str] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    status: Mapped[str] = mapped_column(String(32), default="uploaded", nullable=False)
    rows_total: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    rows_success: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    rows_error: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    comment: Mapped[str | None] = mapped_column(Text())


class ImportRowRaw(Base):
    __tablename__ = "import_rows_raw"

    id: Mapped[int] = mapped_column(primary_key=True)
    file_import_id: Mapped[int] = mapped_column(ForeignKey("file_imports.id", ondelete="CASCADE"), nullable=False)
    sheet_name: Mapped[str | None] = mapped_column(String(255))
    row_number: Mapped[int] = mapped_column(Integer, nullable=False)
    raw_data: Mapped[dict] = mapped_column(JSON, nullable=False)
    parsed_status: Mapped[str] = mapped_column(String(32), default="new", nullable=False)
    error_message: Mapped[str | None] = mapped_column(Text())
    created_at: Mapped[str] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
