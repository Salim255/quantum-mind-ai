from sqlmodel import SQLModel, Field
from uuid import UUID, uuid4
from datetime import datetime, UTC

class QuizAttempt(SQLModel, table=True):
    __tablename__="quiz_attempts"

    id: UUID = Field(
        default_factory=uuid4,
        primary_key=True,
        index=True,
    )

    user_id: UUID = Field(
        nullable=False,
        index=True,
    )

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

    started_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        nullable=False,
    )

    completed_at: datetime | None = Field(
        default=None,
    )