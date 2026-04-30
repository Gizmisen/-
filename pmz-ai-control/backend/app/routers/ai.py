from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.ai import AIQueryRequest, AIQueryResponse
from app.services.ai_service import answer_query, build_document_by_query, get_ai_capabilities
from app.services.audit_service import write_audit

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
