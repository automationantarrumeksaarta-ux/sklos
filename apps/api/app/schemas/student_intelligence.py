from typing import List, Optional

from pydantic import BaseModel


class StudentCardOut(BaseModel):
    """Matches the "Executive Student Card" from the source document §23 —
    everything a mentor needs to understand a student's state at a glance."""

    id: str
    name: str
    dreamTarget: str
    currentScore: int
    targetScore: int
    scoreGap: int
    status: str
    program: Optional[str] = None
    readinessScore: Optional[float] = None
    primaryBottleneck: Optional[str] = None

    class Config:
        from_attributes = True


class TryOutTrendPoint(BaseModel):
    label: str
    totalScore: int


class StudentDetailOut(StudentCardOut):
    school: str
    grade: str
    program: str
    tryOutTrend: List[TryOutTrendPoint] = []
