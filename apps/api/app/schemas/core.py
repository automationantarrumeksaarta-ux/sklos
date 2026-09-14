from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class TaskOut(BaseModel):
    id: str
    title: str
    projectName: str
    dueDate: str
    definitionOfDone: str
    progress: int
    status: str

    class Config:
        from_attributes = True


class DailyUpdateIn(BaseModel):
    taskId: str
    progress: int
    output: str = ""
    impact: str = ""
    energyLevel: int = 3
    nextAction: str = ""
    userId: Optional[str] = "USER-001"


class BlockerIn(BaseModel):
    taskId: str
    description: str
    severity: str = "MEDIUM"
    impact: str = ""
    helpNeeded: str = ""
    userId: Optional[str] = "USER-001"


class SyncRunOut(BaseModel):
    id: str
    sourceFile: str
    inserted: int
    updated: int
    duplicate: int
    review: int
    blocked: int
    createdAt: datetime

    class Config:
        from_attributes = True
