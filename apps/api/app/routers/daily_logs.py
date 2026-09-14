from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.core import AuditLog, DailyLog, Task
from app.schemas.core import DailyUpdateIn

router = APIRouter(prefix="/api/v1/daily-logs", tags=["daily-logs"])


@router.post("", status_code=201)
def create_daily_log(payload: DailyUpdateIn, db: Session = Depends(get_db)):
    task = db.get(Task, payload.taskId)
    if not task:
        raise HTTPException(status_code=404, detail="Task tidak ditemukan")

    log = DailyLog(
        user_id=payload.userId,
        task_id=payload.taskId,
        progress=payload.progress,
        output=payload.output,
        impact=payload.impact,
        energy_level=payload.energyLevel,
        next_action=payload.nextAction,
    )
    db.add(log)

    # Keep the task's own progress and status in sync with the latest log,
    # per PRD v1.2 §10.2 (My Day) — the log is the evidence, the task is
    # the current state.
    task.progress = payload.progress
    if payload.progress >= 100:
        task.status = "DONE"
    elif task.status == "TODO":
        task.status = "IN_PROGRESS"

    db.add(
        AuditLog(
            actor_id=payload.userId,
            action="CREATE_DAILY_LOG",
            entity="task",
            entity_id=payload.taskId,
            after_value=f"progress={payload.progress}",
        )
    )
    db.commit()
    return {"status": "ok", "logId": log.log_id}
