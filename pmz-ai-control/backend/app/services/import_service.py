from pathlib import Path

from sqlalchemy.orm import Session

from app.models.imports import FileImport, ImportRowRaw
from app.models.production_fact import ProductionFact
from app.models.production_plan import ProductionPlan
from app.services.excel_reader import load_sheet, read_file_preview


PLAN_REQUIRED = {"plan_period", "plan_version", "order_number", "planned_qty", "planned_hours"}
FACT_REQUIRED = {"fact_period", "order_number", "fact_qty", "fact_hours"}

PLAN_MAPPING = {
    "Период": "plan_period",
    "Версия": "plan_version",
    "Заказ": "order_number",
    "Номер материала": "material_code",
    "Краткий текст материала": "material_name",
    "Завод": "plant",
    "Участок": "department",
    "Рабочее место": "work_center",
    "Количество": "planned_qty",
    "Общее время": "planned_hours",
}

FACT_MAPPING = {
    "Период": "fact_period",
    "Заказ": "order_number",
    "Заказ клиента": "customer_order",
    "Номер материала": "material_code",
    "Краткий текст материала": "material_name",
    "Завод": "plant",
    "Участок": "department",
    "Рабочее место": "work_center",
    "Количество заказа": "order_qty",
    "ПоставлКоличество": "delivered_qty",
    "Подтвержд. колич-во": "confirmed_qty",
    "ФактКоличество": "fact_qty",
    "ФактЧасы": "fact_hours",
}


def _normalize_df(df, mapping: dict[str, str]):
    cols = {c: mapping.get(c, c) for c in df.columns}
    return df.rename(columns=cols)


def validate_columns(df_columns: set[str], required: set[str]) -> list[str]:
    return sorted(list(required - df_columns))


def save_raw_rows(db: Session, file_import: FileImport) -> int:
    path = Path(file_import.file_path)
    preview = read_file_preview(path, max_rows=1)
    total = 0
    for sheet in preview["sheet_names"]:
        df = load_sheet(path, None if path.suffix.lower() == ".csv" else sheet)
        for idx, row in df.iterrows():
            db.add(ImportRowRaw(file_import_id=file_import.id, sheet_name=sheet, row_number=int(idx) + 1, raw_data=row.fillna("").to_dict()))
            total += 1
    file_import.rows_total = total
    db.commit()
    return total


def import_plan(db: Session, file_import: FileImport, sheet_name: str) -> int:
    path = Path(file_import.file_path)
    df = load_sheet(path, None if path.suffix.lower() == ".csv" else sheet_name)
    df = _normalize_df(df, PLAN_MAPPING)
    missing = validate_columns(set(df.columns), PLAN_REQUIRED)
    if missing:
        raise ValueError(f"Missing required columns for plan import: {', '.join(missing)}")

    count = 0
    for _, r in df.iterrows():
        db.add(ProductionPlan(
            plan_period=str(r.get("plan_period", "")),
            plan_version=str(r.get("plan_version", "BP")),
            order_number=str(r.get("order_number", "")),
            material_code=str(r.get("material_code", "")),
            material_name=str(r.get("material_name", "")),
            plant=str(r.get("plant", "")),
            department=str(r.get("department", "")),
            work_center=str(r.get("work_center", "")),
            planned_qty=float(r.get("planned_qty", 0) or 0),
            planned_hours=float(r.get("planned_hours", 0) or 0),
            planned_weight=float(r.get("planned_weight", 0) or 0),
            source_file_id=file_import.id,
        ))
        count += 1
    file_import.rows_success = count
    file_import.status = "imported"
    db.commit()
    return count


def import_fact(db: Session, file_import: FileImport, sheet_name: str) -> int:
    path = Path(file_import.file_path)
    df = load_sheet(path, None if path.suffix.lower() == ".csv" else sheet_name)
    df = _normalize_df(df, FACT_MAPPING)
    missing = validate_columns(set(df.columns), FACT_REQUIRED)
    if missing:
        raise ValueError(f"Missing required columns for fact import: {', '.join(missing)}")

    count = 0
    for _, r in df.iterrows():
        db.add(ProductionFact(
            fact_period=str(r.get("fact_period", "")),
            order_number=str(r.get("order_number", "")),
            customer_order=str(r.get("customer_order", "")),
            material_code=str(r.get("material_code", "")),
            material_name=str(r.get("material_name", "")),
            plant=str(r.get("plant", "")),
            department=str(r.get("department", "")),
            work_center=str(r.get("work_center", "")),
            order_qty=float(r.get("order_qty", 0) or 0),
            delivered_qty=float(r.get("delivered_qty", 0) or 0),
            confirmed_qty=float(r.get("confirmed_qty", 0) or 0),
            fact_qty=float(r.get("fact_qty", 0) or 0),
            fact_hours=float(r.get("fact_hours", 0) or 0),
            source_file_id=file_import.id,
        ))
        count += 1
    file_import.rows_success = count
    file_import.status = "imported"
    db.commit()
    return count
