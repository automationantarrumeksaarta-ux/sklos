from collections import Counter

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.sessions import MentorCheckIn, PracticeAttempt, TeachingSession
from app.models.student_intelligence import Student

router = APIRouter(prefix="/api/v1/students", tags=["sessions"])


class MentorCheckInIn(BaseModel):
    conditionScore: int = 3
    targetNext3Days: str = ""
    completionEvidence: str = ""
    errorOrBlocker: str = ""
    nextAction: str = ""
    riskStatus: str = "GREEN"
    mentorId: str = "USER-003"


@router.post("/{student_id}/check-ins", status_code=201)
def create_check_in(student_id: str, payload: MentorCheckInIn, db: Session = Depends(get_db)):
    """Check-In Mentor 10 Menit — TEOS manifesto Lampiran D. Quick pulse,
    same cadence role as Quick Daily Update in SKLOS."""
    student = db.get(Student, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Siswa tidak ditemukan")

    check_in = MentorCheckIn(
        student_id=student_id,
        mentor_id=payload.mentorId,
        condition_1to5=payload.conditionScore,
        target_next_3_days=payload.targetNext3Days,
        completion_evidence=payload.completionEvidence,
        error_or_blocker=payload.errorOrBlocker,
        next_action=payload.nextAction,
        risk_status=payload.riskStatus,
    )
    db.add(check_in)
    db.commit()
    return {"status": "ok", "checkInId": check_in.check_in_id}


@router.get("/{student_id}/journey")
def get_student_journey(student_id: str, db: Session = Depends(get_db)):
    """Session Journey (100 Session Tracker) + a short Error Bank summary,
    per docs/02-SELS-and-Tutor-Sync.md §3-4. Kept as one combined endpoint
    for now — split into /sessions and /practice-attempts once either
    grows past what an Executive Student Card needs."""
    student = db.get(Student, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Siswa tidak ditemukan")

    sessions = (
        db.execute(
            select(TeachingSession)
            .where(TeachingSession.student_id == student_id)
            .order_by(TeachingSession.session_number.asc())
        )
        .scalars()
        .all()
    )
    attempts = (
        db.execute(
            select(PracticeAttempt).where(PracticeAttempt.student_id == student_id)
        )
        .scalars()
        .all()
    )

    completed = len(sessions)
    attendance_rate = (
        round(100 * sum(1 for s in sessions if s.attendance) / completed)
        if completed
        else 0
    )
    avg_mastery = round(sum(s.mastery_score for s in sessions) / completed) if completed else 0
    current_stage = sessions[-1].stage if sessions else "FOUNDATION"

    wrong = [a for a in attempts if not a.correct]
    diagnosis_counts = Counter(a.cognitive_diagnosis for a in wrong if a.cognitive_diagnosis)
    top_error_patterns = [
        {"diagnosis": diag, "count": count}
        for diag, count in diagnosis_counts.most_common(3)
    ]

    return {
        "studentId": student_id,
        "completedSessions": completed,
        "currentStage": current_stage,
        "attendanceRate": attendance_rate,
        "averageMastery": avg_mastery,
        "totalPracticeAttempts": len(attempts),
        "topErrorPatterns": top_error_patterns,
    }
