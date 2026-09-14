from __future__ import annotations
from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.database import Base
from app.models.core import gen_id

# Per-track stage boundaries. UTBK corrected in
# docs/04-Kurikulum-100-Sesi-Integration.md §2; PU added in
# docs/06-PU-Mastery-Tracking-Integration.md §1. TKA has no official
# sub-stage in any source document, hence the empty list.
TRACK_SESSION_STAGES = {
    "UTBK": [
        ("FOUNDATION", 1, 21),
        ("MASTERY", 22, 49),
        ("ADVANCED", 50, 63),
        ("INTEGRATION_PEAK", 64, 75),
    ],
    "PU": [
        ("FOUNDATION", 1, 6),
        ("ANALYSIS", 7, 14),
        ("MASTERY", 15, 20),
    ],
    "TKA": [],
}


def stage_for_session(session_number: int, track: str = "UTBK") -> str | None:
    stages = TRACK_SESSION_STAGES.get(track, [])
    if not stages:
        return None  # e.g. TKA — no official sub-stage in the source curricula
    for stage, lo, hi in stages:
        if lo <= session_number <= hi:
            return stage
    return stages[-1][0] if session_number > stages[-1][2] else stages[0][0]


# 6 Golden Key stages from the TEOS manifesto Bab 9 — a cross-subject
# generalization of the Numerasi-specific protocol in
# docs/prompts/socratic-numeracy-tutor.md.
GOLDEN_KEY_STAGES = ["DIAGNOSE", "UNDERSTAND", "REASON", "DETECT", "REPAIR", "RETAIN"]

# 12 cognitive diagnosis categories from the Socratic Numeracy Tutor spec
# §14 — docs/prompts/socratic-numeracy-tutor.md.
COGNITIVE_DIAGNOSES = [
    "CONCEPT_ERROR",
    "MODELING_ERROR",
    "PROCEDURAL_ERROR",
    "ARITHMETIC_ERROR",
    "READING_ERROR",
    "LOGIC_ERROR",
    "WORKING_MEMORY_ERROR",
    "CARELESS_ERROR",
    "STRATEGY_ERROR",
    "GUESSING",
    "OVERTHINKING",
    "PREMATURE_CALCULATION",
]

# 6 mastery statuses from the same spec §18. Target is TRANSFER_MASTERY.
MASTERY_STATUSES = [
    "INTRODUCED",
    "DEVELOPING",
    "UNSTABLE",
    "PROCEDURAL_MASTERY",
    "TRANSFER_MASTERY",
    "AUTOMATIC",
]

# 5 quick tutor-facing Error Clinic categories from the 100-session
# curriculum's lesson plan template (§12) — distinct from the 12-category
# COGNITIVE_DIAGNOSES machine taxonomy above. See
# docs/04-Kurikulum-100-Sesi-Integration.md §4.
ERROR_CLINIC_CATEGORIES = ["KONSEP", "CEROBOH", "STRATEGI", "WAKTU", "EMOSI"]

_DIAGNOSIS_TO_ERROR_CLINIC = {
    "CONCEPT_ERROR": "KONSEP",
    "MODELING_ERROR": "KONSEP",
    "PROCEDURAL_ERROR": "STRATEGI",
    "ARITHMETIC_ERROR": "CEROBOH",
    "READING_ERROR": "CEROBOH",
    "LOGIC_ERROR": "STRATEGI",
    "WORKING_MEMORY_ERROR": "STRATEGI",
    "CARELESS_ERROR": "CEROBOH",
    "STRATEGY_ERROR": "STRATEGI",
    "GUESSING": "EMOSI",
    "OVERTHINKING": "WAKTU",
    "PREMATURE_CALCULATION": "WAKTU",
}


def to_error_clinic_category(cognitive_diagnosis: str | None) -> str | None:
    """Collapses a PracticeAttempt's 12-category machine diagnosis into
    the 5 quick categories a tutor tags in Error Clinic during class."""
    if not cognitive_diagnosis:
        return None
    return _DIAGNOSIS_TO_ERROR_CLINIC.get(cognitive_diagnosis)


# PU-specific taxonomies — SEC_PU_Learning_OS_Skill_v1_0.md §8-9. These
# sit ABOVE the generic taxonomies as extra detail (only defined for PU
# so far); PracticeAttempt.subject_error_code / .subject_trap_code hold
# these as free strings so other domains can define their own catalogs
# later without a schema change. See
# docs/06-PU-Mastery-Tracking-Integration.md §2.
PU_ERROR_CODES = {
    "PU-E1": "Konsep",
    "PU-E2": "Representasi",
    "PU-E3": "Inferensi",
    "PU-E4": "Kuantor",
    "PU-E5": "Negasi",
    "PU-E6": "Implikasi",
    "PU-E7": "Asumsi",
    "PU-E8": "Relevansi",
    "PU-E9": "Kausalitas",
    "PU-E10": "Constraint",
    "PU-E11": "Strategi",
    "PU-E12": "Waktu",
    "PU-E13": "Confidence",
    "PU-E14": "Fokus/Emosi",
}

PU_TRAP_CODES = {
    "PU-R1": "Hubungan dibalik",
    "PU-R2": "Informasi ditambah",
    "PU-R3": "Mungkin dianggap pasti",
    "PU-R4": "Kuantor diperkuat",
    "PU-R5": "'Sebagian' dianggap 'tidak semua'",
    "PU-R6": "Kata sama dianggap hubungan",
    "PU-R7": "Negasi keliru",
    "PU-R8": "Afirmasi konsekuen",
    "PU-R9": "Penyangkalan anteseden",
    "PU-R10": "Korelasi dianggap sebab",
    "PU-R11": "Bukti tidak relevan",
    "PU-R12": "Kesimpulan terlalu luas",
    "PU-R13": "Kesimpulan terlalu sempit",
    "PU-R14": "Intuisi menggantikan premis",
    "PU-R15": "Familiarity trap",
    "PU-R16": "Opsi benar umum, salah konteks",
    "PU-R17": "Soal mahal waktu",
    "PU-R18": "Confidence palsu",
}

# Five-Framework Cheat Sheet — PU Mastery Ebook, Lampiran C.
PU_FRAMEWORKS = ["Argument Audit", "WCC", "T3", "Analytical Grid", "Quantitative Modeling"]


class TeachingSession(Base):
    """One row per class session, following the 10-step lesson template
    from Smarteducafe_Elite_Learning_System_Pengjaran.md. Each step is a
    short tutor note, not a long form — target input time stays under
    30-60 seconds per student (source doc §8 in the earlier SEC OS
    proposal)."""

    __tablename__ = "teaching_sessions"

    session_id = Column(String, primary_key=True, default=lambda: gen_id("TS"))
    student_id = Column(String, ForeignKey("students.student_id"), nullable=False)
    tutor_id = Column(String, ForeignKey("users.user_id"), nullable=True)
    track = Column(String, default="UTBK")  # "TKA" | "UTBK" — separate numbering per track
    session_number = Column(Integer, nullable=False)  # 1-25 for TKA, 1-75 for UTBK
    stage = Column(String, nullable=True)  # from stage_for_session(); None for TKA
    topic = Column(String, default="")
    ai_level = Column(String, nullable=True)  # L1-L6 AI-integration depth per session — see §5 of the sync doc; NOT the same scale as PracticeAttempt.level

    brain_activation = Column(Text, default="")
    mission_brief = Column(Text, default="")
    concept_piercing = Column(Text, default="")
    guided_practice = Column(Text, default="")
    communicative_challenge = Column(Text, default="")
    battle_practice = Column(Text, default="")
    error_clinic = Column(Text, default="")
    reflection = Column(Text, default="")
    daily_mission = Column(Text, default="")
    mentor_review = Column(Text, default="")

    attendance = Column(Boolean, default=True)
    engagement_score = Column(Integer, default=0)  # 0-100
    mastery_score = Column(Integer, default=0)  # 0-100
    assignment_completed = Column(Boolean, default=False)

    created_at = Column(DateTime, default=datetime.utcnow)

    student = relationship("Student")


class PracticeAttempt(Base):
    """One row per drilled question, per the Socratic Numeracy Tutor Error
    Bank (spec §17). This is the data layer for a future AI Coach — no LLM
    call happens here yet; a human tutor or a later AI Coach integration
    writes these rows using the same taxonomy the spec defines."""

    __tablename__ = "practice_attempts"

    attempt_id = Column(String, primary_key=True, default=lambda: gen_id("PA"))
    student_id = Column(String, ForeignKey("students.student_id"), nullable=False)
    domain = Column(String, default="PM")  # PU/PPU/PBM/LBI/LBE/PM
    concept = Column(String, default="")
    level = Column(String, default="L1")  # L1-L6, spec §8
    correct = Column(Boolean, default=False)
    cognitive_diagnosis = Column(String, nullable=True)  # one of COGNITIVE_DIAGNOSES, null if correct
    golden_key_stage = Column(String, nullable=True)  # one of GOLDEN_KEY_STAGES — where the thinking broke
    subject_error_code = Column(String, nullable=True)  # e.g. "PU-E3" — see PU_ERROR_CODES, extra detail atop cognitive_diagnosis
    subject_trap_code = Column(String, nullable=True)  # e.g. "PU-R7" — see PU_TRAP_CODES
    framework_used = Column(String, nullable=True)  # one of PU_FRAMEWORKS, when applicable
    confidence = Column(Integer, default=3)  # 1-5, spec §16
    attempt_number = Column(Integer, default=1)  # 1-3, spec §13
    mastery_status = Column(String, default="INTRODUCED")  # one of MASTERY_STATUSES
    time_seconds = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)

    student = relationship("Student")


class MentorCheckIn(Base):
    """Check-In Mentor 10 Menit from the TEOS manifesto Lampiran D — a
    quick, frequent pulse check, distinct from the deeper/rarer
    `MentoringSession`. Mirrors the same relationship SKLOS already has
    between Quick Daily Update (frequent) and Weekly Review (deep)."""

    __tablename__ = "mentor_check_ins"

    check_in_id = Column(String, primary_key=True, default=lambda: gen_id("CHK"))
    student_id = Column(String, ForeignKey("students.student_id"), nullable=False)
    mentor_id = Column(String, ForeignKey("users.user_id"), nullable=True)
    condition_1to5 = Column(Integer, default=3)
    target_next_3_days = Column(Text, default="")
    completion_evidence = Column(Text, default="")
    error_or_blocker = Column(Text, default="")
    next_action = Column(Text, default="")
    risk_status = Column(String, default="GREEN")  # GREEN | YELLOW | RED — Lampiran E's 3 canonical levels
    created_at = Column(DateTime, default=datetime.utcnow)

    student = relationship("Student")


class CurriculumSession(Base):
    """The syllabus plan — one row per session number per track, from
    SmartEduCafe_Kurikulum_100_Sesi_TKA_UTBK_2026_2027.docx §7/§9. This is
    what SHOULD be taught; `TeachingSession` is what actually happened.
    See docs/04-Kurikulum-100-Sesi-Integration.md §3."""

    __tablename__ = "curriculum_sessions"

    id = Column(String, primary_key=True, default=lambda: gen_id("CUR"))
    track = Column(String, nullable=False)  # "TKA" | "UTBK"
    session_number = Column(Integer, nullable=False)
    domain = Column(String, default="")  # UTBK subtest code, or subject name for TKA
    materi_usp = Column(String, default="")
    outcome = Column(Text, default="")
    stage = Column(String, nullable=True)
