from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.config import settings
from app.database import get_db
from app.models.imports import FileImport
from app.schemas.ai import AIQueryRequest, AIQueryResponse
from app.services.ai_service import answer_query, build_document_by_query, get_ai_capabilities
from app.services.audit_service import write_audit
from app.services.import_service import import_fact, import_plan, save_raw_rows
from app.services.orders_history_import_service import import_orders_history
from app.services.portfolio_import_service import import_portfolio_requests
from app.services.production_data_import_service import import_master_data

router = APIRouter(prefix="/ai", tags=["ai"])


@router.post("/query", response_model=AIQueryResponse)
def query_ai(payload: AIQueryRequest, db: Session = Depends(get_db)):
    answer, data, mode = answer_query(db, payload.query, advanced=payload.advanced)
    write_audit(db, action="ai_query", entity_type="ai_request", new_value={"query": payload.query, "answer": answer, "mode": mode})
    return AIQueryResponse(answer=answer, data=data, mode=mode)


@router.get("/document")
def ai_document(query: str | None = None, db: Session = Depends(get_db)):
    doc = build_document_by_query(db, query=query or "")
    write_audit(db, action="ai_document", entity_type="ai_request", new_value={"query": query, "title": doc.get("title")})
    return doc


@router.get("/capabilities")
def ai_capabilities():
    return get_ai_capabilities()


@router.post("/ingest-file")
async def ai_ingest_file(
    target: str = Form(..., description="plan|fact|production-data|portfolio|orders-history"),
    file: UploadFile = File(...),
    sheet_name: str = Form(default="sheet1"),
    db: Session = Depends(get_db),
):
    uploads_dir = Path(settings.upload_dir)
    uploads_dir.mkdir(parents=True, exist_ok=True)
    ext = Path(file.filename).suffix.lower()
    if ext not in {".xlsx", ".xlsm", ".xls", ".csv"}:
        raise HTTPException(status_code=400, detail="Unsupported file type")

    stored_name = f"{uuid4()}{ext}"
    destination = uploads_dir / stored_name
    destination.write_bytes(await file.read())

    rec = FileImport(file_name=stored_name, original_file_name=file.filename, file_path=str(destination), module=target, file_type=ext)
    db.add(rec)
    db.commit()
    db.refresh(rec)
    save_raw_rows(db, rec)

    t = target.lower().strip()
    try:
        if t == "plan":
            rows = import_plan(db, rec, sheet_name)
        elif t == "fact":
            rows = import_fact(db, rec, sheet_name)
        elif t == "production-data":
            result = import_master_data(db, rec)
            rows = sum(v for k, v in result.items() if isinstance(v, int))
        elif t == "portfolio":
            rows = import_portfolio_requests(db, rec)
        elif t == "orders-history":
            result = import_orders_history(db, rec)
            rows = int(result.get("imported_rows", 0))
        else:
            raise HTTPException(status_code=400, detail="Unsupported target")
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    write_audit(db, action="ai_ingest_file", entity_type="file_import", entity_id=str(rec.id), new_value={"target": target, "rows": rows})
    return {"status": "ok", "file_id": rec.id, "target": target, "rows": rows}
