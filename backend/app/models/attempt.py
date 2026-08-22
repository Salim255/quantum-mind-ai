from __future__ import annotations

from datetime import UTC, datetime
from uuid import UUID, uuid4

from sqlalchemy import Column, DateTime
from sqlmodel import Field, Relationship, SQLModel


class Attempt(SQLModel, table=True):
    """
    Represents one user's attempt at a quiz for a specific topic.

    An attempt belongs to one topic and stores the resulting performance
    of that quiz session.
    """

    __tablename__ = "attempts"

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
    user_id: UUID | None = Field(
        default=None,
        nullable=True,
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
        back_populates="attempts",
    )

    # ============================================================
    # RESULT
    # ============================================================

    score: float = Field(
        default=0.0,
        nullable=False,
    )

    total_questions: int = Field(
        default=0,
        nullable=False,
    )

    correct_answers: int = Field(
        default=0,
        nullable=False,
    )

    # ============================================================
    # STATUS
    # ============================================================

    is_completed: bool = Field(
        default=False,
        nullable=False,
        index=True,
    )

    # ============================================================
    # LIFECYCLE
    # ============================================================

    started_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        sa_column=Column(
            DateTime(timezone=True),
            nullable=False,
        ),
    )

    completed_at: datetime | None = Field(
        default=None,
        sa_column=Column(
            DateTime(timezone=True),
            nullable=True,
        ),
    )