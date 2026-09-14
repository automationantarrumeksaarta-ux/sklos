from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.database import Base
from app.models.core import gen_id

# AI-Kaizen-Operating-System-SmartEduCafe-Iterasi-v2.0.md §5.5-5.6. This
# closes a gap that existed since the very first SKLOS PRD (v1.2 §10.7,
# "Knowledge Chain and SOP") was written but never implemented in code —
# earlier iterations of this basis built the operational layers
# (Task/Blocker/DailyLog, then the student-facing modules) without ever
# adding the Learning -> Knowledge -> SOP pipeline the PRD promised.

LEARNING_STAGES = ["CAPTURED", "IMPLEMENTED", "VALIDATED", "STANDARDIZED", "REUSED"]
LEARNING_CATEGORIES = [
    "MARKETING", "SALES", "OPERASIONAL", "LEADERSHIP", "FINANCE", "LEARNING", "AI", "HR",
]
SOP_STATUSES = ["DRAFT", "TESTED", "APPROVED", "ACTIVE", "RETIRED"]


class LearningEvent(Base):
    """One captured lesson learned — the raw material knowledge starts as.
    Blocker -> LearningEvent -> KnowledgeItem -> SOP is the intended
    pipeline (source doc's Knowledge Chain), same shape SKLOS's PRD
    described from day one but never had a table for."""

    __tablename__ = "learning_events"

    learning_id = Column(String, primary_key=True, default=lambda: gen_id("LRN"))
    project_id = Column(String, ForeignKey("projects.project_id"), nullable=True)
    lesson_learned = Column(Text, nullable=False)
    category = Column(String, nullable=True)  # one of LEARNING_CATEGORIES
    validated_by = Column(String, ForeignKey("users.user_id"), nullable=True)
    reuse_potential = Column(Boolean, default=False)
    learning_stage = Column(String, default="CAPTURED")  # one of LEARNING_STAGES
    knowledge_tag = Column(String, default="")
    owner_id = Column(String, ForeignKey("users.user_id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class KnowledgeItem(Base):
    """A knowledge asset — may or may not become an SOP. Recommending
    'Jadikan SOP' stays a human decision (SOP_status starts at DRAFT and
    is advanced manually), consistent with the Human-in-the-Loop
    principle already held throughout this basis."""

    __tablename__ = "knowledge_items"

    knowledge_id = Column(String, primary_key=True, default=lambda: gen_id("KB"))
    category = Column(String, default="")
    title = Column(String, nullable=False)
    content = Column(Text, default="")
    source_learning_id = Column(String, ForeignKey("learning_events.learning_id"), nullable=True)
    template = Column(Text, default="")
    ai_prompt = Column(Text, default="")
    sop_candidate = Column(Boolean, default=False)
    sop_status = Column(String, default="DRAFT")  # one of SOP_STATUSES
    reuse_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
