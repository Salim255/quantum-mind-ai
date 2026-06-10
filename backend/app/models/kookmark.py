from sqlmodel import SQLModel, Field
from datetime import datetime, UTC
from uuid import UUID, uuid4

class Bookmark(SQLModel, table=True):
    """
    Top-level PDF outline nodes only.
    Example: "1 Spin", "2 Linear Algebra"
    """

    __tablename__ = "bookmarks"

    id: UUID = Field(default_factory=uuid4, primary_key=True)

    document_id: UUID = Field(foreign_key="documents.id", index=True)

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