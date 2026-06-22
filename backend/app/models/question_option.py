from sqlmodel import SQLModel, Field
from datetime import datetime, UTC
from uuid import UUID, uuid4

class QuestionOption(SQLModel, table=True):
    __tablename__="question_options"

    id: UUID = Field(
        default_factory=uuid4,
        primary_key=True,
        index=True,
    )

    question_id: UUID = Field(
        foreign_key="questions.id",
        nullable=False,
        index=True,
    )

    option_text: str = Field(
        nullable=False,
        max_length=1000,
    )

    is_correct: bool = Field(
        default=False,
        nullable=False,
    )

    display_order: int = Field(
        default=0,
        nullable=False,
    )

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        nullable=False
    )

    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        nullable=False
    )