from sqlmodel import SQLModel, Field
from datetime import datetime, UTC
from uuid import UUID, uuid4


class Section(SQLModel, table=True):
    """
    Inner sections that belong to a Bookmark.
    NOT recursive.
    """

    __tablename__ = "sections"

    id: UUID = Field(default_factory=uuid4, primary_key=True)

    bookmark_id: UUID = Field(foreign_key="bookmarks.id", index=True)

    title: str = Field(nullable=False, index=True)

    start_page: int
    end_page: int

    order_index: int = Field(default=0)

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        nullable=False,
    )

    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        nullable=False,
    )