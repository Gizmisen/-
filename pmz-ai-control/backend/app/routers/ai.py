from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.ai import AIQueryRequest, AIQueryResponse
from app.services.audit_service import write_audit
from app.services.ai_service import answer_query

router = APIRouter(prefix="/ai", tags=["ai"])


@router.post("/query", response_model=AIQueryResponse)
def query_ai(payload: AIQueryRequest, db: Session = Depends(get_db)):
    answer, data = answer_query(db, payload.query)
    write_audit(db, action="ai_query", entity_type="ai_request", new_value={"query": payload.query, "answer": answer})
    return AIQueryResponse(answer=answer, data=data)
