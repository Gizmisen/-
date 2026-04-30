from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import Base, engine
from app.models import imports, materials, orders, production_fact, production_plan, users
from app.routers import ai, auth, dashboard, fact, imports as imports_router, labor_fact, orders_history, plan_fact, plan_versions, planning, portfolio, production_data, sales, sap, templates, ui, warehouse


@asynccontextmanager
async def lifespan(_: FastAPI):
    if settings.app_env.lower() in {"dev", "local", "test"}:
        Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(title="PMZ AI Control", version="0.3.0", lifespan=lifespan)

origins = [x.strip() for x in settings.allowed_origins.split(",") if x.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def healthcheck() -> dict[str, str]:
    return {"status": "ok", "instance": settings.instance_name, "env": settings.app_env}


app.include_router(auth.router)
app.include_router(imports_router.router)
app.include_router(plan_fact.router)
app.include_router(ai.router)
app.include_router(ui.router)

app.include_router(templates.router)

app.include_router(production_data.router)
app.include_router(portfolio.router)
app.include_router(orders_history.router)
app.include_router(planning.router)
app.include_router(plan_versions.router)
app.include_router(fact.router)
app.include_router(labor_fact.router)
app.include_router(warehouse.router)
app.include_router(sales.router)
app.include_router(sap.router)
app.include_router(dashboard.router)
