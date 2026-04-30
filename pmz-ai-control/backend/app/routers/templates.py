from pathlib import Path

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

router = APIRouter(prefix="/templates", tags=["templates"])


@router.get("/plan")
def get_plan_template():
    path = Path("app/templates/files/plan_template.csv")
    if not path.exists():
        raise HTTPException(status_code=404, detail="Template not found")
    return FileResponse(path=path, filename="plan_template.csv", media_type="text/csv")


@router.get("/fact")
def get_fact_template():
    path = Path("app/templates/files/fact_template.csv")
    if not path.exists():
        raise HTTPException(status_code=404, detail="Template not found")
    return FileResponse(path=path, filename="fact_template.csv", media_type="text/csv")
