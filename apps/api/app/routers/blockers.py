from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.core import AuditLog, Blocker, Task
from app.schemas.core import BlockerIn

router = APIRouter(prefix="/api/v1/blockers", tags=["blockers"])


@router.post("", status_code=201)
def create_blocker(payload: BlockerIn, db: Session = Depends(get_db)):
    task = db.get(Task, payload.taskId)
    if not task:
        raise HTTPException(status_code=404, detail="Task tidak ditemukan")

    blocker = Blocker(
        task_id=payload.taskId,
        reporter_id=payload.userId,
        description=payload.description,
        severity=payload.severity,
        impact=payload.impact,
        help_needed=payload.helpNeeded,
    )
    db.add(blocker)

    # Per Gemini/Apps Script guide §10 and Local Pilot Guide §2: a stuck
    # report marks the task BLOCKED so it surfaces in the Team Room.
    task.status = "BLOCKED"

    db.add(
        AuditLog(
            actor_id=payload.userId,
            action="CREATE_BLOCKER",
            entity="task",
            entity_id=payload.taskId,
            after_value=f"severity={payload.severity}",
        )
    )
    db.commit()
    return {"status": "ok", "blockerId": blocker.blocker_id}
