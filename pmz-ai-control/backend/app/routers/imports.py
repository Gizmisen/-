from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.config import settings
from app.database import get_db
from app.models.imports import FileImport
from app.services.audit_service import write_audit
from app.services.excel_reader import CSV_SHEET, read_file_preview
from app.services.import_service import import_fact, import_plan, save_raw_rows

router = APIRouter(prefix="/imports", tags=["imports"])


@router.post("/upload")
async def upload_file(module: str = Form(...), file: UploadFile = File(...), db: Session = Depends(get_db)):
    uploads_dir = Path(settings.upload_dir)
    uploads_dir.mkdir(parents=True, exist_ok=True)
    ext = Path(file.filename).suffix.lower()
    if ext not in {".xlsx", ".xlsm", ".xls", ".csv"}:
        raise HTTPException(status_code=400, detail="Unsupported file type")

    stored_name = f"{uuid4()}{ext}"
    destination = uploads_dir / stored_name
    destination.write_bytes(await file.read())

    rec = FileImport(
        file_name=stored_name,
        original_file_name=file.filename,
        file_path=str(destination),
        module=module,
        file_type=ext,
    )
    db.add(rec)
    db.commit()
    db.refresh(rec)

    total = save_raw_rows(db, rec)
    write_audit(db, action="upload_file", entity_type="file_import", entity_id=str(rec.id), new_value={"module": module, "rows_total": total})
    return {"file_id": rec.id, "rows_total": total}


@router.get("/{file_id}/preview")
def preview_file(file_id: int, db: Session = Depends(get_db)):
    rec = db.query(FileImport).filter(FileImport.id == file_id).first()
    if not rec:
        raise HTTPException(status_code=404, detail="File not found")
    return read_file_preview(Path(rec.file_path))


@router.post("/{file_id}/confirm")
def confirm_import(file_id: int, sheet_name: str = Form(default=CSV_SHEET), db: Session = Depends(get_db)):
    rec = db.query(FileImport).filter(FileImport.id == file_id).first()
    if not rec:
        raise HTTPException(status_code=404, detail="File not found")
    module = (rec.module or "").lower()
    try:
        if module == "plan":
            rows = import_plan(db, rec, sheet_name)
        elif module in {"fact", "coois"}:
            rows = import_fact(db, rec, sheet_name)
        else:
            raise HTTPException(status_code=400, detail="Unsupported module for confirm")
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    write_audit(db, action="confirm_import", entity_type="file_import", entity_id=str(rec.id), new_value={"rows": rows, "status": rec.status})
    return {"imported_rows": rows, "status": rec.status}
