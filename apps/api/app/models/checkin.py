from datetime import date, datetime

from sqlalchemy import Boolean, Column, Date, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.database import Base
from app.models.core import gen_id
from app.models.sessions import ERROR_CLINIC_CATEGORIES  # noqa: F401 — re-exported for convenience

# AI Learning levels from SOP_Pedoman_Transformasi_SEC_Elite_700_Plus.pdf
# §10 — corrects the previously-undefined TeachingSession.ai_level scale.
AI_LEVELS = {
    "L1": "Golden Key Solver",
    "L2": "Detektor Kerentanan",
    "L3": "Simulasi Kesalahan Nyata",
    "L4": "Feynman Arena",
    "L5": "Personalized 7-Day Sprint",
    "L6": "Doomsday Simulator",
}

# 7 daily point components from the SOP §12. Max total = 100/day.
POINT_COMPONENTS = {
    "close_day": 10,
    "physical_exercise": 10,
    "focus_target": 20,
    "hots_target": 20,
    "active_recall": 20,
    "ai_learning": 10,
    "reflection": 10,
}


def student_level(total_points_accumulated: int) -> str:
    """Working tier labels — the source SOP shows only one dashboard
    example ("ROOKIE") with no full table. Needs calibration with real
    data before being used for any decision. See
    docs/05-Student-Tracking-Points-Sync.md §3."""
    if total_points_accumulated >= 2000:
        return "ELITE"
    if total_points_accumulated >= 1000:
        return "DISCIPLINED"
    if total_points_accumulated >= 300:
        return "CONSISTENT"
    return "ROOKIE"


def weekly_status(completion_rate: float, sleep_hours: float, stress: int) -> str:
    """Pure function per the SOP's explicit numeric triggers §11.1 —
    unlike StudentRiskScore.status, which is a mentor judgment call, this
    one is fully computable from the inputs."""
    if completion_rate >= 0.80 and sleep_hours >= 7 and stress < 7:
        return "HIJAU"
    if completion_rate < 0.60 or sleep_hours < 6.5 or stress >= 9:
        return "MERAH"
    return "KUNING"


class DailyCheckIn(Base):
    """Student's own daily 5R self-report — SOP §14.1. Distinct from
    MentorCheckIn (mentor-initiated, about the student) and TeachingSession
    (tutor's class log) — this one is student-authored, about themselves,
    the same relationship SKLOS's own DailyLog has to staff."""

    __tablename__ = "daily_check_ins"

    check_in_id = Column(String, primary_key=True, default=lambda: gen_id("DCI"))
    student_id = Column(String, ForeignKey("students.student_id"), nullable=False)
    check_in_date = Column(Date, default=date.today)

    sleep_hours = Column(Float, default=0)
    energy_1to10 = Column(Integer, default=5)
    stress_1to10 = Column(Integer, default=5)

    ready_body_activity = Column(String, default="")
    ready_body_duration_min = Column(Integer, default=0)
    ready_body_rpe = Column(Integer, default=0)  # 1-10

    recall_note = Column(Text, default="")

    reason_questions = Column(Integer, default=0)
    reason_correct = Column(Integer, default=0)
    reason_focus_minutes = Column(Integer, default=0)
    reason_costly_time_count = Column(Integer, default=0)

    error_dominant = Column(String, nullable=True)  # one of ERROR_CLINIC_CATEGORIES

    ai_learning_level = Column(String, nullable=True)  # one of AI_LEVELS keys
    ai_blindspot_or_revision = Column(Text, default="")

    resilience_note = Column(Text, default="")  # "Daya juang" — what did you do after a mistake/difficulty
    recovery_note = Column(Text, default="")
    commitment_tomorrow = Column(Text, default="")

    created_at = Column(DateTime, default=datetime.utcnow)

    student = relationship("Student")


class StudentPoints(Base):
    """One row per student per day — component-level points, not just a
    total, so a dashboard can show which component is chronically missed.
    Deliberately NOT linked to Assessment/TryOut/StudentRiskScore: points
    measure daily process, never academic mastery. See sync doc §3."""

    __tablename__ = "student_points"

    id = Column(String, primary_key=True, default=lambda: gen_id("PTS"))
    student_id = Column(String, ForeignKey("students.student_id"), nullable=False)
    point_date = Column(Date, default=date.today)

    close_day = Column(Integer, default=0)
    physical_exercise = Column(Integer, default=0)
    focus_target = Column(Integer, default=0)
    hots_target = Column(Integer, default=0)
    active_recall = Column(Integer, default=0)
    ai_learning = Column(Integer, default=0)
    reflection = Column(Integer, default=0)

    created_at = Column(DateTime, default=datetime.utcnow)

    student = relationship("Student")

    @property
    def total(self) -> int:
        return (
            self.close_day
            + self.physical_exercise
            + self.focus_target
            + self.hots_target
            + self.active_recall
            + self.ai_learning
            + self.reflection
        )
