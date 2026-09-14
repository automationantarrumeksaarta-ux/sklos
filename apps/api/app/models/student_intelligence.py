from datetime import datetime

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.database import Base
from app.models.core import gen_id

# Default SRS (SEC Readiness Score) weights — copied as-is from the source
# document as a reference formula, NOT a calibrated one. Recalibrate with
# real SEC data before using this for any student-facing decision. See
# docs/01-SEC-Student-Intelligence-Sync.md §4.
SRS_WEIGHTS = {
    "academic_mastery": 0.30,
    "tryout_performance": 0.25,
    "score_momentum": 0.15,
    "learning_consistency": 0.10,
    "attendance": 0.05,
    "task_completion": 0.05,
    "mental_performance": 0.05,
    "target_gap": 0.05,
}

# Corrected to the official UTBK 2026 structure per
# SmartEduCafe_Kurikulum_100_Sesi_TKA_UTBK_2026_2027.docx §2: TPS (PU,
# PPU, PBM, PK) + Tes Literasi (LBI, LBE) + Penalaran Matematika (PM).
# Earlier versions of this basis used 6 domains (missing PK) — fixed here.
UTBK_DOMAINS = ["PU", "PPU", "PBM", "PK", "LBI", "LBE", "PM"]

# 10 elective tracks for TKA sesi 14-21 (kurikulum §8). A TKA student
# picks 2 of these, stored as free text on Student.tka_elective_tracks
# (e.g. "Fisika,Ekonomi") — kept as a constant, not a table, same
# reasoning as PROGRAM_CATALOG below.
TKA_ELECTIVE_TRACKS = [
    "Matematika Tingkat Lanjut",
    "Fisika",
    "Kimia",
    "Biologi",
    "Ekonomi",
    "Sosiologi",
    "Geografi",
    "Sejarah",
    "Pendidikan Pancasila",
    "Bahasa Lanjutan/Asing",
]

# TEOS manifesto Lampiran E locks 3 official Traffic-Light levels for
# parent/management-facing reports. The internal 4-level status
# (GREEN/YELLOW/ORANGE/RED) stays as-is for mentor-facing nuance — see
# docs/03-TEOS-Manifesto-Integration.md §3.
def to_traffic_light(internal_status: str) -> str:
    return {
        "GREEN": "Hijau",
        "YELLOW": "Kuning",
        "ORANGE": "Kuning",
        "RED": "Merah",
    }.get(internal_status, "Kuning")

# From Smarteducafe_Elite_Learning_System_Master_Knowledge_v1.md.
# `Student.program` should store one of these codes as free text — kept as
# a string column (not a DB enum) so new programs don't need a migration,
# validated at the API layer instead.
PROGRAM_CATALOG = {
    "SMART_CLASS": {
        "name": "Smart Class",
        "positioning": "Membangun Cara Belajar yang Benar",
        "score_gain_min": 80,
        "score_gain_max": 100,
    },
    "INTENSIF_CLASS": {
        "name": "Intensif Class",
        "positioning": "Score Acceleration Program",
        "score_gain_min": 100,
        "score_gain_max": 150,
    },
    "EXCLUSIVE_CLASS": {
        "name": "Exclusive Class",
        "positioning": "Personal Success Program",
        "score_gain_min": 180,
        "score_gain_max": 250,
    },
    "EXCLUSIVE_KEDINASAN": {
        "name": "Exclusive + Kedinasan",
        "positioning": "Ultimate Success Program",
        "score_gain_min": None,
        "score_gain_max": None,
    },
}


class Student(Base):
    """Student 360 core record. `mentor_id`/`tutor_id` point at the same
    `users` table SKLOS uses — a Mentor/Tutor logs in once and works in
    both My Day (their own tasks) and Student Room (their students)."""

    __tablename__ = "students"

    student_id = Column(String, primary_key=True, default=lambda: gen_id("SEC"))
    name = Column(String, nullable=False)
    school = Column(String, default="")
    grade = Column(String, default="")
    dream_target = Column(String, default="")  # e.g. "Ilmu Komunikasi UNPAD"
    target_score = Column(Integer, default=0)
    baseline_score = Column(Integer, default=0)
    current_score = Column(Integer, default=0)
    program = Column(String, default="")
    tka_elective_tracks = Column(String, default="")  # e.g. "Fisika,Ekonomi" — see TKA_ELECTIVE_TRACKS
    mentor_id = Column(String, ForeignKey("users.user_id"), nullable=True)
    tutor_id = Column(String, ForeignKey("users.user_id"), nullable=True)
    status = Column(String, default="GREEN")  # GREEN | YELLOW | ORANGE | RED
    created_at = Column(DateTime, default=datetime.utcnow)

    assessments = relationship("Assessment", back_populates="student")
    tryouts = relationship("TryOut", back_populates="student")
    mentoring_sessions = relationship("MentoringSession", back_populates="student")
    risk_scores = relationship("StudentRiskScore", back_populates="student")

    @property
    def score_gap(self) -> int:
        return max(self.target_score - self.current_score, 0)


class Assessment(Base):
    """One snapshot of the four intelligence domains from the source
    document §4: Career, Academic, Learning, Mental Performance."""

    __tablename__ = "assessments"

    assessment_id = Column(String, primary_key=True, default=lambda: gen_id("ASM"))
    student_id = Column(String, ForeignKey("students.student_id"), nullable=False)
    career_score = Column(Integer, default=0)
    academic_score = Column(Integer, default=0)
    learning_score = Column(Integer, default=0)
    mental_score = Column(Integer, default=0)
    notes = Column(Text, default="")
    assessed_at = Column(DateTime, default=datetime.utcnow)

    student = relationship("Student", back_populates="assessments")


class TryOut(Base):
    __tablename__ = "tryouts"

    tryout_id = Column(String, primary_key=True, default=lambda: gen_id("TO"))
    student_id = Column(String, ForeignKey("students.student_id"), nullable=False)
    label = Column(String, default="")  # e.g. "TO 06"
    total_score = Column(Integer, default=0)
    taken_at = Column(DateTime, default=datetime.utcnow)

    student = relationship("Student", back_populates="tryouts")
    domain_scores = relationship("TryOutDomainScore", back_populates="tryout")


class TryOutDomainScore(Base):
    """One row per UTBK domain (PU/PPU/PBM/LBI/LBE/PM) per try out —
    source for the Priority Gap logic in the source document §6."""

    __tablename__ = "tryout_domain_scores"

    id = Column(String, primary_key=True, default=lambda: gen_id("TDS"))
    tryout_id = Column(String, ForeignKey("tryouts.tryout_id"), nullable=False)
    domain = Column(String, nullable=False)  # one of UTBK_DOMAINS
    score = Column(Integer, default=0)

    tryout = relationship("TryOut", back_populates="domain_scores")


class MentoringSession(Base):
    """One-on-one structure from the source document §12:
    Diagnose / Evidence / Intervention / Commitment / Follow-up."""

    __tablename__ = "mentoring_sessions"

    session_id = Column(String, primary_key=True, default=lambda: gen_id("MTG"))
    student_id = Column(String, ForeignKey("students.student_id"), nullable=False)
    mentor_id = Column(String, ForeignKey("users.user_id"), nullable=True)
    diagnose = Column(Text, default="")
    evidence = Column(Text, default="")
    intervention = Column(Text, default="")
    commitment = Column(Text, default="")
    follow_up_date = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    student = relationship("Student", back_populates="mentoring_sessions")


class TransformationIndex(Base):
    """Periodic Parent Trust Dashboard snapshot — 5 indices from Master
    Knowledge v1. Distinct from `Assessment` (point-in-time diagnostic
    intake): this is a recurring report aimed at parents and management,
    not a per-student diagnosis. See docs/02-SELS-and-Tutor-Sync.md §2."""

    __tablename__ = "transformation_indices"

    id = Column(String, primary_key=True, default=lambda: gen_id("TI"))
    student_id = Column(String, ForeignKey("students.student_id"), nullable=False)
    academic_index = Column(Integer, default=0)
    learning_habit_index = Column(Integer, default=0)
    character_index = Column(Integer, default=0)
    leadership_index = Column(Integer, default=0)
    future_readiness_index = Column(Integer, default=0)
    period_label = Column(String, default="")  # e.g. "September 2026"
    created_at = Column(DateTime, default=datetime.utcnow)

    student = relationship("Student")


class StudentRiskScore(Base):
    """Snapshot of the risk radar (GREEN/YELLOW/ORANGE/RED) with the
    reasoning that produced it — every status must stay drill-down-able,
    same auditability principle as Kaizen Score in PRD v1.2 §6."""

    __tablename__ = "student_risk_scores"

    id = Column(String, primary_key=True, default=lambda: gen_id("RISK"))
    student_id = Column(String, ForeignKey("students.student_id"), nullable=False)
    status = Column(String, default="GREEN")
    readiness_score = Column(Float, default=0.0)  # SRS, 0-100, see SRS_WEIGHTS
    primary_bottleneck = Column(String, default="")
    reason = Column(Text, default="")
    computed_at = Column(DateTime, default=datetime.utcnow)

    student = relationship("Student", back_populates="risk_scores")
