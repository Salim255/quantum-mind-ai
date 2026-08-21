from datetime import UTC, datetime
from uuid import UUID, uuid4

from sqlalchemy import Column, DateTime
from sqlmodel import Field, Relationship, SQLModel


class Answer(SQLModel, table=True):
    """
    Represents a possible answer to a learning question.

    An answer belongs to a question and its associated learning topic.
    It contains the information required to present and evaluate
    the answer during an assessment.
    """

    __tablename__ = "answers"

    # ============================================================
    # IDENTITY
    # ============================================================

    id: UUID = Field(
        default_factory=uuid4,
        primary_key=True,
        index=True,
    )

    # ============================================================
    # LEARNING CONTEXT
    # ============================================================

    topic_id: UUID = Field(
        foreign_key="topics.id",
        nullable=False,
        index=True,
    )

    topic: "Topic" = Relationship(
        back_populates="answers",
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
        back_populates="answers",
    )

    # ============================================================
    # CONTENT
    # ============================================================

    text: str = Field(
        nullable=False,
        max_length=1000,
    )

    explanation: str | None = Field(
        default=None,
        max_length=2000,
    )

    # ============================================================
    # ASSESSMENT
    # ============================================================

    is_correct: bool = Field(
        default=False,
        nullable=False,
    )

    # ============================================================
    # PRESENTATION
    # ============================================================

    display_order: int = Field(
        default=0,
        nullable=False,
    )

    # ============================================================
    # STATUS
    # ============================================================

    is_active: bool = Field(
        default=True,
        nullable=False,
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