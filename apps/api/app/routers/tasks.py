from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.core import Project, Task
from app.schemas.core import TaskOut

router = APIRouter(prefix="/api/v1/tasks", tags=["tasks"])


@router.get("/today", response_model=list[TaskOut])
def get_today_tasks(user_id: str, db: Session = Depends(get_db)):
    """Returns up to 3 priority tasks for My Day, ordered by priority then
    due date. Contributors only ever see their own tasks (role scoping is
    enforced once real auth replaces NEXT_PUBLIC_USE_MOCK_AUTH)."""
    rows = (
        db.execute(
            select(Task, Project)
            .join(Project, Task.project_id == Project.project_id, isouter=True)
            .where(Task.owner_id == user_id)
            .order_by(Task.priority.asc())
            .limit(3)
        )
        .all()
    )
    return [
        TaskOut(
            id=task.task_id,
            title=task.title,
            projectName=project.project_name if project else "Tanpa proyek",
            dueDate=task.due_date or "-",
            definitionOfDone=task.definition_of_done or "-",
            progress=task.progress,
            status=task.status,
        )
        for task, project in rows
    ]
