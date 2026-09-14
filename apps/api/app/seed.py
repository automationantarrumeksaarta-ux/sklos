"""Seed dummy data for the local pilot. Run with:

    python -m app.seed

Only dummy names are used here — never load real patient or therapy data
through this script (see PRD v1.2 §39, §12 of the Local Pilot Guide).
"""

from app.database import Base, SessionLocal, engine
from app.models.core import Project, Task, User

Base.metadata.create_all(bind=engine)
db = SessionLocal()

try:
    if db.query(User).count() == 0:
        khaila = User(user_id="USER-001", name="Khaila", email="khaila@example.com", role="CONTRIBUTOR")
        ridho = User(user_id="USER-002", name="Ridho", email="ridho@example.com", role="CONTRIBUTOR")
        lead = User(user_id="USER-003", name="Team Lead", email="lead@example.com", role="TEAM_LEADER")
        admin = User(user_id="USER-004", name="Local Admin", email="admin@example.com", role="ADMIN")
        db.add_all([khaila, ridho, lead, admin])
        db.flush()

        pilot = Project(project_id="PRJ-PILOT", project_name="SKLOS Local Pilot", owner_id="USER-003")
        kurikulum = Project(project_id="PRJ-KURIKULUM", project_name="Kurikulum Foundation", owner_id="USER-003")
        marketing = Project(project_id="PRJ-MARKETING", project_name="Marketing SmartEduCafe", owner_id="USER-003")
        db.add_all([pilot, kurikulum, marketing])

        db.add_all(
            [
                Task(
                    task_id="TSK-001",
                    project_id="PRJ-MARKETING",
                    owner_id="USER-001",
                    title="Campaign Foundation — brief konten",
                    definition_of_done="3 draft caption + 1 moodboard visual disetujui lead",
                    due_date="Besok",
                    priority=1,
                    status="IN_PROGRESS",
                    progress=60,
                ),
                Task(
                    task_id="TSK-002",
                    project_id="PRJ-PILOT",
                    owner_id="USER-001",
                    title="Uji My Day dengan 2 contributor",
                    definition_of_done="Feedback usability dicatat di Team Room",
                    due_date="Hari ini",
                    priority=2,
                    status="TODO",
                    progress=20,
                ),
                Task(
                    task_id="TSK-003",
                    project_id="PRJ-KURIKULUM",
                    owner_id="USER-001",
                    title="Review modul Numerasi minggu 3",
                    definition_of_done="Checklist QA modul terisi penuh",
                    due_date="Lusa",
                    priority=3,
                    status="IN_PROGRESS",
                    progress=80,
                ),
            ]
        )

        db.commit()
        print("Seed selesai: 4 user, 3 project, 3 task.")
    else:
        print("Users sudah ada, seed dilewati.")
finally:
    db.close()
