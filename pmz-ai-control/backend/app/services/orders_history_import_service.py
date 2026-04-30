import json
from pathlib import Path

from sqlalchemy.orm import Session

from app.models.extended_contour import OrdersHistory, OrdersHistoryRawRow
from app.models.imports import FileImport
from app.services.excel_reader import load_sheet, read_file_preview

SHEET_HINTS = ("СЗ", "услуг", "график", "потреб")


def import_orders_history(db: Session, file_import: FileImport) -> dict:
    path = Path(file_import.file_path)
    preview = read_file_preview(path, max_rows=1)
    sheets = preview.get("sheet_names", [])
    imported = 0
    used_sheets = []

    for sheet in sheets:
        if not any(h.lower() in sheet.lower() for h in SHEET_HINTS):
            continue
        df = load_sheet(path, sheet)
        used_sheets.append(sheet)
        for idx, r in df.iterrows():
            db.add(OrdersHistoryRawRow(file_import_id=file_import.id, sheet_name=sheet, row_number=int(idx) + 1, raw_data=json.dumps(r.fillna("").to_dict(), ensure_ascii=False), detected_profile="auto", parse_status="parsed"))
            order_number = str(r.get("Заказ") or r.get("order_number") or "").strip()
            status = str(r.get("Статус") or r.get("status") or "").strip() or None
            comment = str(r.get("Примечание") or r.get("comment") or sheet).strip() or sheet
            if not order_number:
                continue
            db.add(OrdersHistory(
                source_sheet=sheet,
                source_row_number=int(idx) + 1,
                plant=str(r.get("Завод") or "") or None,
                customer_name=str(r.get("Заказчик") or "") or None,
                material_code=str(r.get("ОЗМ") or r.get("Материал") or "") or None,
                material_name=str(r.get("Наименование") or "") or None,
                qty=float(r.get("колич") or 0),
                order_number=order_number,
                status=status,
                comment=comment,
            ))
            imported += 1

    file_import.status = "imported"
    file_import.rows_success = imported
    db.commit()
    return {"imported_rows": imported, "sheets": used_sheets}
