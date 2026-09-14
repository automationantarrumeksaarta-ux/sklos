import uuid
from datetime import datetime, timedelta

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import relationship

from app.database import Base


def gen_id(prefix: str) -> str:
    return f"{prefix}-{uuid.uuid4().hex[:8].upper()}"


# AI-Kaizen-Operating-System-SmartEduCafe-Iterasi-v2.0.md §7.1 — Base
# Priority = Impact x Urgency (each 1-5). Task.impact_score/.urgency_score
# feed this; Task.priority (the ordinal My Day already sorts by) is set
# separately and can be informed by this classification, not replaced by
# it — see docs/07-Master-ERP-Architecture.md.
def compute_priority(impact_score: int, urgency_score: int) -> str:
    score = impact_score * urgency_score
    if score >= 16:
        return "P1_CRITICAL"
    if score >= 10:
        return "P2_HIGH"
    if score >= 5:
        return "P3_MEDIUM"
    return "P4_LOW"


class User(Base):
    __tablename__ = "users"

    user_id = Column(String, primary_key=True, default=lambda: gen_id("USER"))
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    role = Column(String, nullable=False, default="CONTRIBUTOR")  # CONTRIBUTOR | TEAM_LEADER | ADMIN
    team_id = Column(String, nullable=True)
    active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class Project(Base):
    __tablename__ = "projects"

    project_id = Column(String, primary_key=True, default=lambda: gen_id("PRJ"))
    project_name = Column(String, nullable=False)
    owner_id = Column(String, ForeignKey("users.user_id"), nullable=True)
    health_status = Column(String, default="ON_TRACK")
    created_at = Column(DateTime, default=datetime.utcnow)


class Task(Base):
    __tablename__ = "tasks"

    task_id = Column(String, primary_key=True, default=lambda: gen_id("TSK"))
    project_id = Column(String, ForeignKey("projects.project_id"), nullable=True)
    owner_id = Column(String, ForeignKey("users.user_id"), nullable=True)
    title = Column(String, nullable=False)
    definition_of_done = Column(Text, default="")
    due_date = Column(String, nullable=True)
    priority = Column(Integer, default=3)  # 1 = highest, shown in My Day top 3
    status = Column(String, default="TODO")  # TODO | IN_PROGRESS | BLOCKED | DONE
    verification_status = Column(String, nullable=True)  # NOT_REVIEWED | REVIEW_NEEDED | REVISION_REQUIRED | VERIFIED | REJECTED — separate dimension from `status`; "Done" is not "Verified"
    impact_score = Column(Integer, nullable=True)  # 1-5, for compute_priority()
    urgency_score = Column(Integer, nullable=True)  # 1-5, for compute_priority()
    progress = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)

    daily_logs = relationship("DailyLog", back_populates="task")
    blockers = relationship("Blocker", back_populates="task")


class DailyLog(Base):
    __tablename__ = "daily_logs"

    log_id = Column(String, primary_key=True, default=lambda: gen_id("LOG"))
    user_id = Column(String, ForeignKey("users.user_id"), nullable=False)
    task_id = Column(String, ForeignKey("tasks.task_id"), nullable=False)
    progress = Column(Integer, nullable=False)
    output = Column(Text, default="")
    impact = Column(Text, default="")
    energy_level = Column(Integer, default=3)
    next_action = Column(Text, default="")
    created_at = Column(DateTime, default=datetime.utcnow)

    task = relationship("Task", back_populates="daily_logs")


class Blocker(Base):
    __tablename__ = "blockers"

    blocker_id = Column(String, primary_key=True, default=lambda: gen_id("BLK"))
    task_id = Column(String, ForeignKey("tasks.task_id"), nullable=False)
    reporter_id = Column(String, ForeignKey("users.user_id"), nullable=True)
    description = Column(Text, nullable=False)
    severity = Column(String, default="MEDIUM")  # LOW | MEDIUM | HIGH
    impact = Column(Text, default="")
    help_needed = Column(Text, default="")
    status = Column(String, default="OPEN")  # OPEN | INVESTIGATING | CORRECTIVE_ACTION_RUNNING | RESOLVED | VERIFIED_CLOSED
    root_cause_category = Column(String, nullable=True)  # Human | Process | System | Technology | Knowledge | Policy | Communication
    recurrence_flag = Column(Boolean, default=False)
    opened_at = Column(DateTime, default=datetime.utcnow)
    resolved_at = Column(DateTime, nullable=True)

    task = relationship("Task", back_populates="blockers")

    @property
    def is_overdue(self) -> bool:
        """>24h since opened and not yet resolved — the escalation rule
        from TEOS manifesto Bab 19 ('blocked lebih dari 24 jam
        dieskalasikan'), which SKLOS's Team Room already implied."""
        if self.resolved_at is not None:
            return False
        return (datetime.utcnow() - self.opened_at) > timedelta(hours=24)


class StagingActivity(Base):
    """Landing zone for imported spreadsheet rows. Never a source for
    active tasks until reviewed — see PRD v1.2 §31-38."""

    __tablename__ = "stg_activities"

    record_uuid = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    source_workbook = Column(String, nullable=False)
    source_sheet = Column(String, nullable=False)
    source_row = Column(Integer, nullable=False)
    source_hash = Column(String, nullable=False)
    sync_status = Column(String, default="REVIEW")  # READY | REVIEW | BLOCKED | SYNCED
    privacy_sensitive = Column(Boolean, default=False)
    ai_allowed = Column(Boolean, default=True)
    source_payload = Column(Text, default="")
    created_at = Column(DateTime, default=datetime.utcnow)


class SyncRun(Base):
    __tablename__ = "sync_runs"

    sync_run_id = Column(String, primary_key=True, default=lambda: gen_id("SYNC"))
    source_file = Column(String, nullable=False)
    inserted = Column(Integer, default=0)
    updated = Column(Integer, default=0)
    duplicate = Column(Integer, default=0)
    review = Column(Integer, default=0)
    blocked = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)


class AuditLog(Base):
    __tablename__ = "audit_logs"

    audit_id = Column(String, primary_key=True, default=lambda: gen_id("AUD"))
    actor_id = Column(String, nullable=True)
    action = Column(String, nullable=False)
    entity = Column(String, nullable=False)
    entity_id = Column(String, nullable=False)
    before_value = Column(Text, default="")
    after_value = Column(Text, default="")
    created_at = Column(DateTime, default=datetime.utcnow)
