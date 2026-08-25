from __future__ import annotations

from datetime import UTC, datetime
from typing import Any
from uuid import UUID, uuid4

from sqlalchemy import Column, DateTime, Numeric, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB
from sqlmodel import Field, Relationship, SQLModel


class AttemptQuestion(SQLModel, table=True):
    """
    Represents one question presented during a quiz attempt.

    The parent Attempt represents the overall quiz session.

    Each AttemptQuestion stores the complete lifecycle of one
    question during that quiz, including:

    - the question shown to the user
    - the question position
    - the submitted answer
    - correctness and score
    - response time
    - hints and explanations
    - confidence
    - selection metadata

    A question may appear only once within the same attempt.
    """

    __tablename__ = "attempt_questions"

    __table_args__ = (
        UniqueConstraint(
            "quiz_attempt_id",
            "question_id",
            name="uq_attempt_question",
        ),
        UniqueConstraint(
            "quiz_attempt_id",
            "position",
            name="uq_attempt_question_position",
        ),
    )

    # ============================================================
    # IDENTITY
    # ============================================================

    id: UUID = Field(
        default_factory=uuid4,
        primary_key=True,
        index=True,
    )

    # ============================================================
    # ATTEMPT
    # ============================================================

    attempt_id: UUID = Field(
        foreign_key="attempts.id",
        nullable=False,
        index=True,
    )

    attempt: "Attempt" = Relationship(
        back_populates="attempt_questions",
    )

    # ============================================================
    # QUESTION
    # ============================================================

    question_id: UUID = Field(
        foreign_key="questions.id",
        nullable=False,
        index=True,
    )

    question: "Question" = Relationship(
        back_populates="attempt_questions",
    )

    position: int = Field(
        nullable=False,
        index=True,
        description=(
            "Position of the question inside the quiz attempt."
        ),
    )

    # ============================================================
    # QUESTION SNAPSHOT
    # ============================================================

    question_snapshot: dict[str, Any] | None = Field(
        default=None,
        sa_column=Column(
            JSONB,
            nullable=True,
        ),
    )

    question_version: int | None = Field(
        default=None,
        nullable=True,
    )

    difficulty_at_attempt: int | None = Field(
        default=None,
        nullable=True,
    )

    concept_id: UUID | None = Field(
        default=None,
        nullable=True,
        index=True,
    )

    # ============================================================
    # QUESTION LIFECYCLE
    # ============================================================

    presented_at: datetime | None = Field(
        default=None,
        sa_column=Column(
            DateTime(timezone=True),
            nullable=True,
        ),
    )

    started_at: datetime | None = Field(
        default=None,
        sa_column=Column(
            DateTime(timezone=True),
            nullable=True,
        ),
    )

    submitted_at: datetime | None = Field(
        default=None,
        sa_column=Column(
            DateTime(timezone=True),
            nullable=True,
        ),
    )

    # ============================================================
    # ANSWERS
    # ============================================================

    user_answer: dict[str, Any] | None = Field(
        default=None,
        sa_column=Column(
            JSONB,
            nullable=True,
        ),
    )

    correct_answer: dict[str, Any] | None = Field(
        default=None,
        sa_column=Column(
            JSONB,
            nullable=True,
        ),
    )

    # ============================================================
    # RESULT
    # ============================================================

    is_correct: bool | None = Field(
        default=None,
        nullable=True,
        index=True,
    )

    score: float = Field(
        default=0.0,
        sa_column=Column(
            Numeric(5, 2),
            nullable=False,
        ),
    )

    # ============================================================
    # RESPONSE TIME
    # ============================================================

    time_spent_ms: int | None = Field(
        default=None,
        nullable=True,
    )

    # ============================================================
    # HINTS
    # ============================================================

    hint_used: bool = Field(
        default=False,
        nullable=False,
    )

    hint_opened_at: datetime | None = Field(
        default=None,
        sa_column=Column(
            DateTime(timezone=True),
            nullable=True,
        ),
    )

    # ============================================================
    # EXPLANATION
    # ============================================================

    explanation_viewed: bool = Field(
        default=False,
        nullable=False,
    )

    # ============================================================
    # CONFIDENCE
    # ============================================================

    confidence: int | None = Field(
        default=None,
        nullable=True,
    )

    # ============================================================
    # USER HISTORY
    # ============================================================

    attempt_number_for_question: int = Field(
        default=1,
        nullable=False,
    )

    # ============================================================
    # QUESTION SELECTION
    # ============================================================

    selection_reason: str | None = Field(
        default=None,
        max_length=255,
        nullable=True,
    )

    selection_score: float | None = Field(
        default=None,
        sa_column=Column(
            Numeric(8, 3),
            nullable=True,
        ),
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