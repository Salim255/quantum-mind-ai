from datetime import UTC, datetime
from uuid import UUID, uuid4

from sqlalchemy import Column, DateTime
from sqlmodel import Field, Relationship, SQLModel


class Answer(SQLModel, table=True):
    """
    Represents a selectable answer belonging to a question.

    An answer defines the text displayed to the user and whether
    selecting it is considered correct for its question.
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
    # QUESTION RELATIONSHIP
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
    # OPTION CONTENT
    # ============================================================

    option_text: str = Field(
        nullable=False,
        max_length=1000,
    )

    # ============================================================
    # CORRECTNESS
    # ============================================================

    is_correct: bool = Field(
        default=False,
        nullable=False,
    )

    # ============================================================
    # DISPLAY
    # ============================================================

    display_order: int = Field(
        default=0,
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