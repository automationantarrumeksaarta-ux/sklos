"""Seed dummy SEC Student Intelligence data. Run with:

    python -m app.seed_students

Dummy names only — see docs/01-SEC-Student-Intelligence-Sync.md §6.
Never load real student assessment or mental-performance data through
this script before privacy classification is applied to these tables.
"""

from app.database import Base, SessionLocal, engine
from datetime import date, timedelta

from app.models.checkin import DailyCheckIn, StudentPoints
from app.models.sessions import MentorCheckIn, PracticeAttempt, TeachingSession, stage_for_session
from app.models.student_intelligence import (
    MentoringSession,
    Student,
    StudentRiskScore,
    TransformationIndex,
    TryOut,
    TryOutDomainScore,
)

Base.metadata.create_all(bind=engine)
db = SessionLocal()

try:
    if db.query(Student).count() == 0:
        dila = Student(
            student_id="SEC-2026-00124",
            name="Dila",
            school="SMAN 1 Karanganyar",
            grade="12",
            dream_target="Ilmu Komunikasi UNPAD",
            target_score=700,
            baseline_score=500,
            current_score=557,
            program="INTENSIF_CLASS",
            mentor_id="USER-003",
            status="YELLOW",
        )
        keyla = Student(
            student_id="SEC-2026-00131",
            name="Keyla",
            school="SMAN 1 Karanganyar",
            grade="12",
            dream_target="Kriminologi UI",
            target_score=650,
            baseline_score=380,
            current_score=420,
            program="EXCLUSIVE_CLASS",
            mentor_id="USER-003",
            status="ORANGE",
        )
        db.add_all([dila, keyla])
        db.flush()

        to_scores = [402, 438, 471, 496, 528, 557]
        for i, score in enumerate(to_scores, start=1):
            to = TryOut(student_id=dila.student_id, label=f"TO {i:02d}", total_score=score)
            db.add(to)
            db.flush()
            db.add_all(
                [
                    TryOutDomainScore(tryout_id=to.tryout_id, domain="PU", score=score // 6 + 20),
                    TryOutDomainScore(tryout_id=to.tryout_id, domain="LBE", score=score // 6 - 15),
                    TryOutDomainScore(tryout_id=to.tryout_id, domain="PM", score=score // 6 - 25),
                ]
            )

        db.add(
            MentoringSession(
                student_id=dila.student_id,
                mentor_id="USER-003",
                diagnose="Skor stagnan di sekitar Penalaran Matematika.",
                evidence="3 try out terakhir menunjukkan PM di bawah rata-rata domain lain.",
                intervention="PM intensive + weekly TO + mentor check-in.",
                commitment="30 soal PM/hari, 7 hari.",
            )
        )

        db.add_all(
            [
                StudentRiskScore(
                    student_id=dila.student_id,
                    status="YELLOW",
                    readiness_score=67,
                    primary_bottleneck="Penalaran Matematika",
                    reason="Target gap tinggi, attendance baik, PM mastery rendah.",
                ),
                StudentRiskScore(
                    student_id=keyla.student_id,
                    status="ORANGE",
                    readiness_score=48,
                    primary_bottleneck="Penalaran Matematika",
                    reason="UTBK stagnan 410-430, latihan tidak konsisten, confidence turun saat TO.",
                ),
            ]
        )

        db.add(
            TransformationIndex(
                student_id=dila.student_id,
                academic_index=68,
                learning_habit_index=74,
                character_index=61,
                leadership_index=55,
                future_readiness_index=63,
                period_label="September 2026",
            )
        )

        for i in range(1, 38):
            db.add(
                TeachingSession(
                    student_id=dila.student_id,
                    tutor_id="USER-002",
                    session_number=i,
                    stage=stage_for_session(i),
                    topic="Penalaran Matematika" if i % 2 == 0 else "Literasi Bahasa Indonesia",
                    attendance=True,
                    engagement_score=78,
                    mastery_score=65 + (i % 10),
                    assignment_completed=i % 3 != 0,
                )
            )

        practice_seed = [
            ("PM", "L2", True, None, None, 4),
            ("PM", "L3", False, "CONCEPT_ERROR", "UNDERSTAND", 2),
            ("PM", "L3", False, "ARITHMETIC_ERROR", "REPAIR", 3),
            ("PM", "L2", True, None, None, 4),
            ("LBE", "L2", False, "READING_ERROR", "DETECT", 3),
        ]
        for domain, level, correct, diagnosis, gk_stage, confidence in practice_seed:
            db.add(
                PracticeAttempt(
                    student_id=dila.student_id,
                    domain=domain,
                    level=level,
                    correct=correct,
                    cognitive_diagnosis=diagnosis,
                    golden_key_stage=gk_stage,
                    confidence=confidence,
                    mastery_status="DEVELOPING",
                )
            )

        db.add(
            MentorCheckIn(
                student_id=dila.student_id,
                mentor_id="USER-003",
                condition_1to5=4,
                target_next_3_days="Selesaikan 3 set drilling PM + 1 TO mini.",
                completion_evidence="2 dari 3 set drilling selesai, TO mini belum.",
                error_or_blocker="Masih ragu di soal rasio bertingkat.",
                next_action="Review Golden Key tahap Reason untuk soal rasio, besok pagi.",
                risk_status="YELLOW",
            )
        )

        for offset, (completion_quality, error_dom) in enumerate(
            [("good", "STRATEGI"), ("ok", "CEROBOH"), ("good", None)]
        ):
            day = date.today() - timedelta(days=2 - offset)
            db.add(
                DailyCheckIn(
                    student_id=dila.student_id,
                    check_in_date=day,
                    sleep_hours=7.5 if completion_quality == "good" else 6.0,
                    energy_1to10=7,
                    stress_1to10=6 if completion_quality == "good" else 8,
                    ready_body_activity="Mobility + march",
                    ready_body_duration_min=15,
                    ready_body_rpe=4,
                    recall_note="Rasio bertingkat, basis persen, radar jebakan waktu.",
                    reason_questions=15,
                    reason_correct=12 if completion_quality == "good" else 9,
                    reason_focus_minutes=75,
                    reason_costly_time_count=2,
                    error_dominant=error_dom,
                    ai_learning_level="L1",
                    ai_blindspot_or_revision="Masih lemah di rasio bertingkat.",
                    resilience_note="Reset napas setelah 2 soal salah, lanjut lagi.",
                    recovery_note="Tidur 8 jam, screen-off jam 21.30.",
                    commitment_tomorrow="Drilling PM 30 soal + TO mini.",
                )
            )
            db.add(
                StudentPoints(
                    student_id=dila.student_id,
                    point_date=day,
                    close_day=10,
                    physical_exercise=10,
                    focus_target=20 if completion_quality == "good" else 10,
                    hots_target=20 if completion_quality == "good" else 15,
                    active_recall=20,
                    ai_learning=10,
                    reflection=10,
                )
            )

        db.commit()
        print(
            "Seed selesai: 2 siswa, 6 try out, 1 mentoring session, 2 risk score, "
            "1 transformation index, 37 teaching session, 5 practice attempt, 1 check-in mentor, "
            "3 daily check-in siswa, 3 hari poin."
        )
    else:
        print("Students sudah ada, seed dilewati.")
finally:
    db.close()
