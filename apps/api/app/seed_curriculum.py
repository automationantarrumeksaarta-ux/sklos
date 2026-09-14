"""Seed a representative subset of the 100-session curriculum. Run with:

    python -m app.seed_curriculum

Not all 100 rows are typed in here — that is data entry, not an
architecture decision. See docs/04-Kurikulum-100-Sesi-Integration.md §3
for how to extend this from docs/references/Kurikulum-100-Sesi-TKA-UTBK.md.
"""

from app.database import Base, SessionLocal, engine
from app.models.sessions import CurriculumSession, stage_for_session
from app.models.student_intelligence import Student

Base.metadata.create_all(bind=engine)
db = SessionLocal()

try:
    if db.query(CurriculumSession).count() == 0:
        tka_rows = [
            (1, "TKA Terpadu", "Orientasi", "Siswa memahami aturan TKA, kontrak belajar, dan menentukan 3 prioritas awal."),
            (2, "Bahasa Indonesia", "Gagasan utama & struktur teks", "Menentukan gagasan yang paling mewakili bacaan."),
            (3, "Matematika", "Bilangan & relasi", "Menguasai relasi bilangan dan strategi hitung efisien."),
        ]
        for num, domain, materi, outcome in tka_rows:
            db.add(
                CurriculumSession(
                    track="TKA",
                    session_number=num,
                    domain=domain,
                    materi_usp=materi,
                    outcome=outcome,
                    stage=stage_for_session(num, track="TKA"),
                )
            )

        # Full first spiral round of the 75-session UTBK track — one pass
        # through all 7 subtests, per kurikulum §9.
        utbk_rows = [
            (1, "PU", "Baseline dan arsitektur penalaran", "Memahami induktif-deduktif-kuantitatif dan memetakan baseline."),
            (2, "PPU", "Makna kata dan kosakata dalam konteks", "Menentukan makna leksikal/kontekstual dan pilihan kata."),
            (3, "PBM", "Gagasan utama, judul, dan pelengkap gagasan", "Memilih gagasan yang paling mewakili bacaan."),
            (4, "PK", "Number sense dan operasi efisien", "Menghitung, mengestimasi, dan memilih strategi mental."),
            (5, "LBI", "SEC 4 Box dan peta teks", "Memetakan topik, fungsi, bukti, dan hubungan teks."),
            (6, "LBE", "Reading strategy dan vocabulary in context", "Membaca selektif serta memahami kosakata kontekstual."),
            (7, "PM", "Formulating: konteks menjadi model matematika", "Mengubah masalah dunia nyata ke representasi matematika."),
        ]
        for num, domain, materi, outcome in utbk_rows:
            db.add(
                CurriculumSession(
                    track="UTBK",
                    session_number=num,
                    domain=domain,
                    materi_usp=materi,
                    outcome=outcome,
                    stage=stage_for_session(num, track="UTBK"),
                )
            )

        # Full 20-session PU track — SEC_PU_Learning_OS_Skill_v1_0.md §11.
        # (month, stage, session_a_title, session_b_title)
        pu_months = [
            (1, "FOUNDATION", "Pernyataan berkuantor (Logic Detective)", "Silogisme kategorial dasar"),
            (2, "FOUNDATION", "Implikasi dan jika-maka (Security Protocol)", "Negasi, kontraposisi, ekuivalensi"),
            (3, "FOUNDATION", "Silogisme multi-premis (Courtroom Evidence)", "Deductive Logic Challenge"),
            (4, "ANALYSIS", "Generalisasi (Survey Investigator)", "Analogi dan pola kesamaan"),
            (5, "ANALYSIS", "Struktur sebab-akibat (Newsroom Fact Check)", "Menjelaskan perbedaan kondisi"),
            (6, "ANALYSIS", "Memperkuat argumen (Shark Tank Evidence)", "Memperlemah dan asumsi"),
            (7, "ANALYSIS", "Membaca data (Data Intelligence Room)", "Evidence-based argument"),
            (8, "MASTERY", "Mixed Logic I (Logic Escape Room)", "Mixed Logic II"),
            (9, "MASTERY", "Time strategy (Tournament)", "PU Tournament"),
            (10, "MASTERY", "Personal blindspot repair (Personal War Room)", "Final PU simulation dan transfer"),
        ]
        for month, stage, session_a, session_b in pu_months:
            sesi_a_num = (month - 1) * 2 + 1
            sesi_b_num = sesi_a_num + 1
            db.add(
                CurriculumSession(
                    track="PU",
                    session_number=sesi_a_num,
                    domain="PU",
                    materi_usp=f"Episode A — {session_a}",
                    outcome="Build the Skill: diagnostic, concept piercing, modeling, guided practice.",
                    stage=stage,
                )
            )
            db.add(
                CurriculumSession(
                    track="PU",
                    session_number=sesi_b_num,
                    domain="PU",
                    materi_usp=f"Episode B — {session_b}",
                    outcome="Apply and Challenge: retrieval, stimulus baru, Boss Fight, Error Clinic, monthly mastery.",
                    stage=stage,
                )
            )

        db.commit()
        print(
            "Seed selesai: 3 sesi TKA, 7 sesi UTBK (satu putaran spiral penuh), 20 sesi PU (penuh)."
        )
    else:
        print("Curriculum sessions sudah ada, seed dilewati.")
finally:
    db.close()
