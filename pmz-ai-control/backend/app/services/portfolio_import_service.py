from pathlib import Path

from sqlalchemy.orm import Session

from app.models.extended_contour import OrderPortfolio
from app.models.imports import FileImport
from app.services.excel_reader import load_sheet


def import_portfolio_requests(db: Session, file_import: FileImport, sheet_name: str = "Заявки на изготовление") -> int:
    path = Path(file_import.file_path)
    df = load_sheet(path, sheet_name)
    count = 0
    for _, r in df.iterrows():
        order_number = str(r.get("заказ") or r.get("order_number") or "").strip()
        material_code = str(r.get("ОЗМ") or r.get("material_code") or "").strip()
        plant = str(r.get("завод") or r.get("plant") or "").strip() or None
        period = str(r.get("месяц") or r.get("period") or "").strip() or ""
        qty = float(r.get("колич") or r.get("qty") or 0)
        if not material_code:
            continue
        db.add(OrderPortfolio(period=period, order_number=order_number or material_code, material_code=material_code, material_name=str(r.get("Наименование") or "") or None, plant=plant, qty=qty))
        count += 1
    file_import.rows_success = count
    file_import.status = "imported"
    db.commit()
    return count
