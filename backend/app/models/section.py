from datetime import datetime, UTC
from uuid import UUID, uuid4
from sqlalchemy import Column, DateTime
from sqlmodel import Relationship, SQLModel, Field


class Section(SQLModel, table=True):
    """
    Represents a learning section inside a Topic.

    A section is a structural unit of a learning topic.
    It organizes the lesson into meaningful chapters that users
    can navigate, bookmark, and scroll through.

    A section DOES NOT contain the actual educational content.

    Content is stored separately as blocks:

        Topic
          |
          └── Section
                 |
                 └── Blocks

    Example:

        Topic:
            "Vectors"

        Sections:
            - Vector Basics
            - Row and Column Vectors
            - Bras and Kets

        Blocks:
            - Heading
            - Paragraph
            - Equation
            - Example
            - Exercise
    """

    __tablename__ = "sections"


    # ==========================================================
    # IDENTITY
    # ==========================================================

    id: UUID = Field(
        default_factory=uuid4,
        primary_key=True,
        index=True,
        description="Unique identifier of the learning section."
    )

    # ==========================================================
    # DISPLAY INFORMATION
    # ==========================================================

    title: str = Field(
        max_length=255,
        nullable=False,
        index=True,
        description=(
            "Human-readable section title displayed in navigation "
            "and learning pages. "
            "Example: 'Introduction to Vectors'."
        )
    )


    slug: str = Field(
        max_length=255,
        nullable=False,
        index=True,
        description=(
            "URL-friendly identifier used for section navigation "
            "and deep linking. "
            "Example: 'introduction-to-vectors'."
        )
    )


    description: str | None = Field(
        default=None,
        nullable=True,
        description=(
            "Short explanation of what this section teaches. "
            "Used in previews and navigation summaries."
        )
    )


    # ==========================================================
    # ORDERING
    # ==========================================================

    order_index: int = Field(
        default=0,
        nullable=False,
        description=(
            "Controls the position of this section inside its parent topic."
        )
    )



    # ==========================================================
    # PARENT RELATIONSHIP
    # ==========================================================

    topic_id: UUID = Field(
        foreign_key="topics.id",
        nullable=False,
        index=True,
        description=(
            "Identifier of the parent topic that owns this section."
        ),
    )

    topic: "Topic" = Relationship(
        back_populates="sections",
    )
    """
    Parent learning topic that owns this section.

    Relationship:

        Topic
            └── Sections

    Every section belongs to exactly one topic.
    """
    
    # ==========================================================
    # CHILD RELATIONSHIP
    # ==========================================================

    blocks: list["Block"] = Relationship(
        back_populates="section",
        cascade_delete=True,
    )
    """
    Collection of educational content blocks belonging to this section.

    Relationship:

        Topic
            |
            └── Section
                    |
                    └── Blocks


    A section can contain zero or many blocks.

    Blocks are the smallest renderable learning units,
    such as:

        - heading
        - paragraph
        - equation
        - image
        - example
        - exercise


    Cascade behavior:

    When a section is deleted:
        - all related blocks are automatically deleted.

    This prevents orphan blocks without a valid parent section.
    """

    # ==========================================================
    # AUDIT
    # ==========================================================

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        sa_column=Column(
            DateTime(timezone=True),
            nullable=False,
        ),
        description="Timestamp when the section was created."
    )


    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        sa_column=Column(
            DateTime(timezone=True),
            nullable=False,
        ),
        description="Timestamp when the section was last updated."
    )