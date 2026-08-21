from __future__ import annotations

from datetime import UTC, datetime
from enum import Enum
from uuid import UUID, uuid4

from sqlalchemy import Column, DateTime
from sqlmodel import Field, Relationship, SQLModel


# ============================================================
# ENUMS
# ============================================================

class QuestionDifficulty(str, Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"


class QuestionSource(str, Enum):
    MANUAL = "manual"
    AI = "ai"
    IMPORTED = "imported"


# ============================================================
# QUESTION
# ============================================================

class Question(SQLModel, table=True):
    """
    Represents a learning question belonging to a topic.

    A question contains the learning content presented to the learner,
    its assessment metadata, and the answers that can be selected.
    """

    __tablename__ = "questions"

    # ============================================================
    # IDENTITY
    # ============================================================

    id: UUID = Field(
        default_factory=uuid4,
        primary_key=True,
        index=True,
    )

    # ============================================================
    # TOPIC
    # ============================================================

    topic_id: UUID = Field(
        foreign_key="topics.id",
        nullable=False,
        index=True,
    )

    topic: "Topic" = Relationship(
        back_populates="questions",
    )

    # ============================================================
    # CONTENT
    # ============================================================

    text: str = Field(
        nullable=False,
        max_length=2000,
    )

    explanation: str | None = Field(
        default=None,
        max_length=5000,
    )

    # ============================================================
    # ASSESSMENT
    # ============================================================

    difficulty: QuestionDifficulty = Field(
        default=QuestionDifficulty.EASY,
        nullable=False,
        index=True,
    )

    # ============================================================
    # PRESENTATION
    # ============================================================

    display_order: int = Field(
        default=0,
        nullable=False,
    )

    # ============================================================
    # CONTENT SOURCE
    # ============================================================

    source: QuestionSource = Field(
        default=QuestionSource.MANUAL,
        nullable=False,
        max_length=20,
    )

    # ============================================================
    # STATUS
    # ============================================================

    is_active: bool = Field(
        default=True,
        nullable=False,
        index=True,
    )

    # ============================================================
    # ANSWERS
    # ============================================================

    answers: list["Answer"] = Relationship(
        back_populates="question",
    )

    # ============================================================
    # AUDIT
    # ============================================================

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        sa_column=Column(
            DateTime(timezone=True),
            nullable=False,
        ),
    )

    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        sa_column=Column(
            DateTime(timezone=True),
            nullable=False,
        ),
    )