from __future__ import annotations
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.student_intelligence import Student, StudentRiskScore, TryOut
from app.schemas.student_intelligence import (
    StudentCardOut,
    StudentDetailOut,
    TryOutTrendPoint,
)

router = APIRouter(prefix="/api/v1/students", tags=["students"])


def _latest_risk(db: Session, student_id: str) -> StudentRiskScore | None:
    return (
        db.execute(
            select(StudentRiskScore)
            .where(StudentRiskScore.student_id == student_id)
            .order_by(StudentRiskScore.computed_at.desc())
            .limit(1)
        )
        .scalars()
        .first()
    )


@router.get("", response_model=list[StudentCardOut])
def list_students(db: Session = Depends(get_db)):
    """Executive Student Card list — see source document §23. Mentor/Tutor
    scoping (only their own students) is intentionally not enforced yet in
    this pilot scaffold; add it once real auth replaces the mock role."""
    students = db.execute(select(Student)).scalars().all()
    out = []
    for s in students:
        risk = _latest_risk(db, s.student_id)
        out.append(
            StudentCardOut(
                id=s.student_id,
                name=s.name,
                dreamTarget=s.dream_target,
                currentScore=s.current_score,
                targetScore=s.target_score,
                scoreGap=s.score_gap,
                status=risk.status if risk else s.status,
                program=s.program,
                readinessScore=risk.readiness_score if risk else None,
                primaryBottleneck=risk.primary_bottleneck if risk else None,
            )
        )
    return out


@router.get("/{student_id}", response_model=StudentDetailOut)
def get_student(student_id: str, db: Session = Depends(get_db)):
    student = db.get(Student, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Siswa tidak ditemukan")

    risk = _latest_risk(db, student_id)
    tryouts = (
        db.execute(
            select(TryOut)
            .where(TryOut.student_id == student_id)
            .order_by(TryOut.taken_at.asc())
        )
        .scalars()
        .all()
    )

    return StudentDetailOut(
        id=student.student_id,
        name=student.name,
        dreamTarget=student.dream_target,
        currentScore=student.current_score,
        targetScore=student.target_score,
        scoreGap=student.score_gap,
        status=risk.status if risk else student.status,
        readinessScore=risk.readiness_score if risk else None,
        primaryBottleneck=risk.primary_bottleneck if risk else None,
        school=student.school,
        grade=student.grade,
        program=student.program,
        tryOutTrend=[
            TryOutTrendPoint(label=t.label, totalScore=t.total_score) for t in tryouts
        ],
    )
