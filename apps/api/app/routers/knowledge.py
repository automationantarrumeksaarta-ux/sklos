from __future__ import annotations
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.knowledge import KnowledgeItem, LearningEvent

router = APIRouter(prefix="/api/v1/knowledge", tags=["knowledge"])


class LearningEventIn(BaseModel):
    projectId: str | None = None
    lessonLearned: str
    category: str | None = None
    reusePotential: bool = False
    knowledgeTag: str = ""
    ownerId: str | None = None


@router.post("/learning-events", status_code=201)
def create_learning_event(payload: LearningEventIn, db: Session = Depends(get_db)):
    """Capture step of the pipeline — Blocker/retro insight becomes a
    LearningEvent here; promoting it to a KnowledgeItem/SOP stays a
    separate, human-reviewed step (see models/knowledge.py)."""
    event = LearningEvent(
        project_id=payload.projectId,
        lesson_learned=payload.lessonLearned,
        category=payload.category,
        reuse_potential=payload.reusePotential,
        knowledge_tag=payload.knowledgeTag,
        owner_id=payload.ownerId,
    )
    db.add(event)
    db.commit()
    return {"status": "ok", "learningId": event.learning_id}


@router.get("/learning-events")
def list_learning_events(db: Session = Depends(get_db)):
    rows = db.execute(select(LearningEvent).order_by(LearningEvent.created_at.desc())).scalars().all()
    return [
        {
            "id": r.learning_id,
            "lessonLearned": r.lesson_learned,
            "category": r.category,
            "learningStage": r.learning_stage,
            "reusePotential": r.reuse_potential,
            "knowledgeTag": r.knowledge_tag,
        }
        for r in rows
    ]


@router.get("/items")
def list_knowledge_items(db: Session = Depends(get_db)):
    rows = db.execute(select(KnowledgeItem).order_by(KnowledgeItem.created_at.desc())).scalars().all()
    return [
        {
            "id": r.knowledge_id,
            "title": r.title,
            "category": r.category,
            "sopCandidate": r.sop_candidate,
            "sopStatus": r.sop_status,
            "reuseCount": r.reuse_count,
        }
        for r in rows
    ]
