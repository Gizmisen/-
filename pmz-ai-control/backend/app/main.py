from fastapi import FastAPI

from app.database import Base, engine
from app.models import imports, materials, orders, production_fact, production_plan, users
from app.routers import ai, auth, imports as imports_router, plan_fact, ui

app = FastAPI(title="PMZ AI Control", version="0.2.0")


@app.on_event("startup")
def on_startup() -> None:
    Base.metadata.create_all(bind=engine)


@app.get("/health")
def healthcheck() -> dict[str, str]:
    return {"status": "ok"}


app.include_router(auth.router)
app.include_router(imports_router.router)
app.include_router(plan_fact.router)

app.include_router(ai.router)

app.include_router(ui.router)
