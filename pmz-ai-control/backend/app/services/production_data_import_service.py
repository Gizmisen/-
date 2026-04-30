from pathlib import Path

from sqlalchemy.orm import Session

from app.models.extended_contour import BomSpec, RoutingOperation
from app.models.imports import FileImport
from app.models.materials import Material
from app.services.excel_reader import load_sheet


def _path(file_import: FileImport) -> Path:
    return Path(file_import.file_path)


def import_master_data(db: Session, file_import: FileImport) -> dict:
    path = _path(file_import)
    result = {"materials": 0, "specs": 0, "routings": 0}

    errors: list[str] = []

    try:
        materials_df = load_sheet(path, "Изделия")
        for _, r in materials_df.iterrows():
            code = str(r.get("Номер материала") or r.get("material_code") or "").strip()
            name = str(r.get("Краткий текст материала") or r.get("material_name") or "").strip()
            plant = str(r.get("Завод") or r.get("plant") or "").strip() or None
            if not code or not name:
                continue
            exists = db.query(Material).filter(Material.material_code == code, Material.plant == plant).first()
            if exists:
                continue
            db.add(Material(material_code=code, material_name=name, plant=plant, unit=str(r.get("Базисная ЕИ") or "") or None))
            result["materials"] += 1
    except Exception as e:
        errors.append(f"materials: {e}")

    try:
        specs_df = load_sheet(path, "спецификации")
        for _, r in specs_df.iterrows():
            parent = str(r.get("Номер материала") or r.get("parent_material_code") or "").strip()
            component = str(r.get("Компонент") or r.get("component_code") or "").strip()
            if not parent or not component:
                continue
            db.add(BomSpec(parent_material_code=parent, plant=str(r.get("Завод") or "") or None, component_code=component, component_qty=float(r.get("Количество компонента", 0) or 0), component_unit=str(r.get("ЕИ компонента") or "") or None))
            result["specs"] += 1
    except Exception as e:
        errors.append(f"specs: {e}")

    try:
        routes_df = load_sheet(path, "техкарты")
        for _, r in routes_df.iterrows():
            material_code = str(r.get("Номер материала") or r.get("material_code") or "").strip()
            wc = str(r.get("Рабочее место") or r.get("work_center") or "").strip()
            if not material_code or not wc:
                continue
            db.add(RoutingOperation(material_code=material_code, plant=str(r.get("Завод") or "") or None, work_center=wc, labor_value=float(r.get("Заданное значение", 0) or 0), labor_unit="h"))
            result["routings"] += 1
    except Exception as e:
        errors.append(f"routings: {e}")

    db.commit()
    file_import.status = "imported" if not errors else "imported_with_errors"
    file_import.rows_success = sum(result.values())
    db.commit()
    if errors:
        result["errors"] = errors
    return result
