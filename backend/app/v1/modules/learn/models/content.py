from sqlmodel import SQLModel, Field
from datetime import datetime, UTC
from uuid import UUID, uuid4

class Content(SQLModel, table=True):
    """
    Raw extracted PDF text.
    Always tied to a BookmarkSection.
    """

    __tablename__ = "bookmark_section_contents"

    id: UUID = Field(default_factory=uuid4, primary_key=True)

    section_id: UUID = Field(
        foreign_key="bookmark_sections.id",
        unique=True,
        index=True
    )

    content: str

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        nullable=False,
    )

    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        nullable=False,
    )