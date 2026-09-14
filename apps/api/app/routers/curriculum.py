from __future__ import annotations
from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.sessions import CurriculumSession

router = APIRouter(prefix="/api/v1/curriculum", tags=["curriculum"])


@router.get("")
def list_curriculum(track: str | None = None, db: Session = Depends(get_db)):
    """The syllabus plan (what should be taught), not the execution log.
    See docs/04-Kurikulum-100-Sesi-Integration.md §3."""
    query = select(CurriculumSession).order_by(
        CurriculumSession.track, CurriculumSession.session_number
    )
    if track:
        query = query.where(CurriculumSession.track == track)
    rows = db.execute(query).scalars().all()
    return [
        {
            "track": r.track,
            "sessionNumber": r.session_number,
            "domain": r.domain,
            "materiUsp": r.materi_usp,
            "outcome": r.outcome,
            "stage": r.stage,
        }
        for r in rows
    ]
