from __future__ import annotations
from sqlmodel import SQLModel, Field
from uuid import UUID, uuid4
from datetime import datetime, timezone

class Question(SQLModel, table=True):
    __tablename__ = "questions"

    id: UUID = Field(
        default_factory=uuid4,
        primary_key=True,
        index=True
    )

    topic_id: UUID = Field(
        foreign_key="topics.id",
        index=True
    )

    question_text: str = Field(
        nullable=False,
        max_length=2000
    )

    difficulty: str = Field(
        default="easy",
        max_length=20,
        index=True
    )

    explanation: str = Field(
        default=None,
        max_length=5000
    )

    source: str = Field(
        default="manual",
        max_length=50,
    )

    is_active: bool = Field(
        default=True,
        index=True
    )

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        nullable=False
    )