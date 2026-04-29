from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import Base, engine
from app.models import imports, materials, orders, production_fact, production_plan, users
from app.routers import ai, auth, imports as imports_router, plan_fact, ui

app = FastAPI(title="PMZ AI Control", version="0.2.0")

origins = [x.strip() for x in settings.allowed_origins.split(",") if x.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins or ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup() -> None:
    Base.metadata.create_all(bind=engine)


@app.get("/health")
def healthcheck() -> dict[str, str]:
    return {"status": "ok", "instance": settings.instance_name}


app.include_router(auth.router)
app.include_router(imports_router.router)
app.include_router(plan_fact.router)

app.include_router(ai.router)

app.include_router(ui.router)
