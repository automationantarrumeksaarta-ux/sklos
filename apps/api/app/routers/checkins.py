from __future__ import annotations
from datetime import date

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.checkin import POINT_COMPONENTS, DailyCheckIn, StudentPoints, student_level
from app.models.student_intelligence import Student

router = APIRouter(prefix="/api/v1/students", tags=["check-ins"])


class DailyCheckInIn(BaseModel):
    sleepHours: float = 0
    energy: int = 5
    stress: int = 5
    readyBodyActivity: str = ""
    readyBodyDurationMin: int = 0
    readyBodyRpe: int = 0
    recallNote: str = ""
    reasonQuestions: int = 0
    reasonCorrect: int = 0
    reasonFocusMinutes: int = 0
    reasonCostlyTimeCount: int = 0
    errorDominant: str | None = None
    aiLearningLevel: str | None = None
    aiBlindspotOrRevision: str = ""
    resilienceNote: str = ""
    recoveryNote: str = ""
    commitmentTomorrow: str = ""
    # Points earned for this day — 0 to the max listed in POINT_COMPONENTS
    # per component; caller (mentor/system) assigns these based on what
    # was actually completed, this endpoint just records them alongside
    # the check-in it belongs to.
    points: dict[str, int] = {}


@router.post("/{student_id}/daily-check-ins", status_code=201)
def create_daily_check_in(student_id: str, payload: DailyCheckInIn, db: Session = Depends(get_db)):
    """Student's own 5R self-report — SOP §14.1."""
    student = db.get(Student, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Siswa tidak ditemukan")

    check_in = DailyCheckIn(
        student_id=student_id,
        sleep_hours=payload.sleepHours,
        energy_1to10=payload.energy,
        stress_1to10=payload.stress,
        ready_body_activity=payload.readyBodyActivity,
        ready_body_duration_min=payload.readyBodyDurationMin,
        ready_body_rpe=payload.readyBodyRpe,
        recall_note=payload.recallNote,
        reason_questions=payload.reasonQuestions,
        reason_correct=payload.reasonCorrect,
        reason_focus_minutes=payload.reasonFocusMinutes,
        reason_costly_time_count=payload.reasonCostlyTimeCount,
        error_dominant=payload.errorDominant,
        ai_learning_level=payload.aiLearningLevel,
        ai_blindspot_or_revision=payload.aiBlindspotOrRevision,
        resilience_note=payload.resilienceNote,
        recovery_note=payload.recoveryNote,
        commitment_tomorrow=payload.commitmentTomorrow,
    )
    db.add(check_in)

    if payload.points:
        capped = {
            component: max(0, min(value, POINT_COMPONENTS.get(component, 0)))
            for component, value in payload.points.items()
            if component in POINT_COMPONENTS
        }
        db.add(StudentPoints(student_id=student_id, **capped))

    db.commit()
    return {"status": "ok", "checkInId": check_in.check_in_id}


@router.get("/{student_id}/points-summary")
def get_points_summary(student_id: str, db: Session = Depends(get_db)):
    student = db.get(Student, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Siswa tidak ditemukan")

    rows = (
        db.execute(select(StudentPoints).where(StudentPoints.student_id == student_id))
        .scalars()
        .all()
    )
    total = sum(r.total for r in rows)
    return {
        "studentId": student_id,
        "daysTracked": len(rows),
        "totalPoints": total,
        "averagePerDay": round(total / len(rows), 1) if rows else 0,
        "level": student_level(total),
    }
