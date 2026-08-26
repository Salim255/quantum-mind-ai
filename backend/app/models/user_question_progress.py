from __future__ import annotations

from datetime import UTC, datetime
from uuid import UUID, uuid4

from sqlalchemy import Boolean, Column, DateTime, Integer, Numeric
from sqlmodel import Field, Relationship, SQLModel


class UserQuestionProgress(SQLModel, table=True):
    """
    Represents a user's long-term learning progress for a single question.

    Each record tracks how a specific user performs over time on a specific
    question. The data can be used to calculate:

    - accuracy
    - learning mastery
    - correct and incorrect streaks
    - response time
    - spaced repetition
    - review scheduling
    - question difficulty for the individual user
    - question selection priority
    - learning weaknesses

    A user can have one progress record per question.

    Anonymous users do not have persistent progress records.
    """

    __tablename__ = "user_question_progress"

    # ============================================================
    # IDENTITY
    # ============================================================

    id: UUID = Field(
        default_factory=uuid4,
        primary_key=True,
        index=True,
    )

    # ============================================================
    # OWNERSHIP
    # ============================================================

    user_id: UUID = Field(
        nullable=False,
        index=True,
    )

    # ============================================================
    # QUESTION
    # ============================================================

    question_id: UUID = Field(
        foreign_key="questions.id",
        nullable=False,
        index=True,
    )

    question: "Question" = Relationship()

    # ============================================================
    # EXPOSURE
    # ============================================================

    first_seen_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        sa_column=Column(
            DateTime(timezone=True),
            nullable=False,
        ),
    )

    last_seen_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        sa_column=Column(
            DateTime(timezone=True),
            nullable=False,
        ),
    )

    # ============================================================
    # ATTEMPT COUNTS
    # ============================================================

    attempt_count: int = Field(
        default=0,
        nullable=False,
    )

    correct_count: int = Field(
        default=0,
        nullable=False,
    )

    incorrect_count: int = Field(
        default=0,
        nullable=False,
    )

    # ============================================================
    # ACCURACY
    # ============================================================

    accuracy: float = Field(
        default=0.0,
        sa_column=Column(
            Numeric(5, 2),
            nullable=False,
        ),
    )

    last_result: bool | None = Field(
        default=None,
        nullable=True,
    )

    # ============================================================
    # STREAKS
    # ============================================================

    consecutive_correct: int = Field(
        default=0,
        nullable=False,
    )

    consecutive_incorrect: int = Field(
        default=0,
        nullable=False,
    )

    best_streak: int = Field(
        default=0,
        nullable=False,
    )

    # ============================================================
    # RESPONSE TIME
    # ============================================================

    total_time_ms: int = Field(
        default=0,
        nullable=False,
    )

    average_time_ms: int = Field(
        default=0,
        nullable=False,
    )

    fastest_time_ms: int | None = Field(
        default=None,
        nullable=True,
    )

    slowest_time_ms: int | None = Field(
        default=None,
        nullable=True,
    )

    # ============================================================
    # LEARNING BEHAVIOR
    # ============================================================

    hints_used: int = Field(
        default=0,
        nullable=False,
    )

    explanations_viewed: int = Field(
        default=0,
        nullable=False,
    )

    confidence_avg: float | None = Field(
        default=None,
        sa_column=Column(
            Numeric(4, 2),
            nullable=True,
        ),
    )

    # ============================================================
    # MASTERY
    # ============================================================

    mastery_score: float = Field(
        default=0.0,
        sa_column=Column(
            Numeric(6, 3),
            nullable=False,
        ),
    )

    mastery_level: int = Field(
        default=0,
        nullable=False,
    )

    mastered_at: datetime | None = Field(
        default=None,
        sa_column=Column(
            DateTime(timezone=True),
            nullable=True,
        ),
    )

    # ============================================================
    # QUESTION DIFFICULTY FOR USER
    # ============================================================

    difficulty_estimate: float = Field(
        default=0.0,
        sa_column=Column(
            Numeric(5, 2),
            nullable=False,
        ),
    )

    last_difficulty: int | None = Field(
        default=None,
        nullable=True,
    )

    # ============================================================
    # SPACED REPETITION
    # ============================================================

    stability_days: float = Field(
        default=0.0,
        sa_column=Column(
            Numeric(8, 2),
            nullable=False,
        ),
    )

    retrievability: float = Field(
        default=0.0,
        sa_column=Column(
            Numeric(6, 4),
            nullable=False,
        ),
    )

    next_review_at: datetime | None = Field(
        default=None,
        sa_column=Column(
            DateTime(timezone=True),
            nullable=True,
            index=True,
        ),
   
    )

    review_count: int = Field(
        default=0,
        nullable=False,
    )

    overdue: bool = Field(
        default=False,
        sa_column=Column(
            Boolean,
            nullable=False,
            index=True
        ),
    )

    # ============================================================
    # PRIORITIZATION
    # ============================================================

    weakness_score: float = Field(
        default=0.0,
        sa_column=Column(
            Numeric(6, 3),
            nullable=False,
        ),
    )

    priority_score: float = Field(
        default=0.0,
        sa_column=Column(
            Numeric(8, 3),
            nullable=False,
        ),
    )

    last_priority_calculated_at: datetime | None = Field(
        default=None,
        sa_column=Column(
            DateTime(timezone=True),
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

    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        sa_column=Column(
            DateTime(timezone=True),
            nullable=False,
        ),
    )