from sqlmodel import SQLModel, Field
from uuid import UUID, uuid4
from datetime import datetime, UTC

class QuizAttemptAnswer(SQLModel, table=True):
    __tablename__="quiz_attempt_answer"

    id: UUID = Field(
        default_factory=uuid4,
        primary_key=True,
        index=True,
    )

    attempt_id: UUID = Field(
        foreign_key="quiz_attempts.id",
        nullable=False,
        index=True,
    )

    question_id: UUID = Field(
        foreign_key="questions.id",
        nullable=False,
        index=True,
    )

    selected_option_id: UUID | None = Field(
        default=None,
        foreign_key="question_options.id",
    )

    is_correct: bool = Field(
        nullable=False,
    )

    answered_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        nullable=False,
    )