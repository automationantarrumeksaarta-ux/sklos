from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import Base, engine
from app.models import checkin as _checkin_models  # noqa: F401
from app.models import knowledge as _knowledge_models  # noqa: F401
from app.models import sessions as _sessions_models  # noqa: F401
from app.models import student_intelligence as _student_intelligence_models  # noqa: F401
from app.routers import blockers, checkins, curriculum, daily_logs, imports, knowledge, sessions, students, tasks

app = FastAPI(title="SKLOS API", version="1.2.0-pilot")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(tasks.router)
app.include_router(daily_logs.router)
app.include_router(blockers.router)
app.include_router(imports.router)
app.include_router(students.router)
app.include_router(sessions.router)
app.include_router(curriculum.router)
app.include_router(checkins.router)
app.include_router(knowledge.router)


@app.on_event("startup")
def on_startup():
    # Pilot convenience only. Once the schema stabilizes, replace with
    # Alembic migrations (see apps/api/alembic/ and Local Pilot Guide §11)
    # instead of create_all.
    Base.metadata.create_all(bind=engine)


@app.get("/health")
def health():
    return {"status": "ok", "environment": settings.environment}
