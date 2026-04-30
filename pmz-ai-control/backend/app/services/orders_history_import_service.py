from pathlib import Path

from sqlalchemy.orm import Session

from app.models.extended_contour import OrdersHistory
from app.models.imports import FileImport
from app.services.excel_reader import read_file_preview, load_sheet


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
        for _, r in df.iterrows():
            order_number = str(r.get("Заказ") or r.get("order_number") or "").strip()
            status = str(r.get("Статус") or r.get("status") or "").strip() or None
            comment = str(r.get("Примечание") or r.get("comment") or sheet).strip() or sheet
            if not order_number:
                continue
            db.add(OrdersHistory(order_number=order_number, status=status, comment=comment))
            imported += 1

    file_import.status = "imported"
    file_import.rows_success = imported
    db.commit()
    return {"imported_rows": imported, "sheets": used_sheets}
