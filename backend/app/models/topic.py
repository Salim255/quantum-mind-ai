from datetime import datetime, UTC
from uuid import UUID, uuid4

from sqlmodel import SQLModel, Field


class Topic(SQLModel, table=True):
    """
    Represents a learning topic available within QuantumMind.

    A topic is a top-level educational resource that can be
    displayed inside the Learn section and later associated
    with quizzes, exercises, progress tracking, and bookmarks.
    """

    __tablename__ = "topics"

    id: UUID = Field(
        default_factory=uuid4,
        primary_key=True,
        index=True,
    )

    title: str = Field(
        max_length=255,
        nullable=False,
        index=True,
    )

    slug: str = Field(
        max_length=255,
        nullable=False,
        unique=True,
        index=True,
    )

    category: str = Field(
        max_length=100,
        nullable=False,
        index=True,
    )

    content: str = Field(
        nullable=False,
    )

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        nullable=False,
    )

    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        nullable=False,
    )