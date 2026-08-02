from datetime import datetime, UTC
from uuid import UUID, uuid4

from sqlmodel import Relationship, SQLModel, Field

from app.models.section import Section


class Topic(SQLModel, table=True):
    """
    Represents a top-level learning topic inside QuantumMind.

    A Topic is the entry point of a learning resource.

    It is responsible for:

    - Defining the public learning route.
    - Organizing topics by category.
    - Providing the metadata displayed in the Learn section.
    - Owning the collection of learning sections.

    A Topic DOES NOT contain the educational content itself.

    Educational content is organized as:

        Topic
            |
            └── Sections
                    |
                    └── Blocks

    Example:

        Topic:
            "Quantum Entanglement"

        Sections:
            - Introduction
            - Quantum Correlations
            - Bell's Inequality

        Blocks:
            - Paragraph
            - Equation
            - Example
            - Exercise
    """

    __tablename__ = "topics"

    # ==========================================================
    # IDENTITY
    # ==========================================================

    id: UUID = Field(
        default_factory=uuid4,
        primary_key=True,
        index=True,
        description="Unique identifier of the learning topic.",
    )

    # ==========================================================
    # DISPLAY INFORMATION
    # ==========================================================

    title: str = Field(
        max_length=255,
        nullable=False,
        index=True,
        description=(
            "Human-readable title displayed to learners."
        ),
    )

    slug: str = Field(
        max_length=255,
        nullable=False,
        unique=True,
        index=True,
        description=(
            "Stable URL-friendly identifier used for routing and public URLs."
        ),
    )

    description: str | None = Field(
        default=None,
        nullable=True,
        description=(
            "Short introduction displayed before entering the topic."
        ),
    )

    # ==========================================================
    # ORGANIZATION
    # ==========================================================

    category: str = Field(
        max_length=100,
        nullable=False,
        index=True,
        description=(
            "High-level category used to organize learning topics."
        ),
    )

    display_order: int = Field(
        default=0,
        nullable=False,
        description=(
            "Display order of this topic inside its category."
        ),
    )

    # ==========================================================
    # RELATIONSHIPS
    # ==========================================================

    sections: list["Section"] = Relationship(
        back_populates="topic",
        sa_relationship_kwargs={
            "cascade": "all, delete-orphan",
        },
    )
    """
    Collection of learning sections that belong to this topic.

    Relationship:

        Topic
            └── Sections

    A topic can contain zero or many sections.

    Each section belongs to exactly one topic.

    SQLAlchemy automatically manages the lifecycle of child
    sections through this relationship.

    Cascade behavior:

    - save newly added sections
    - update existing sections
    - delete all sections when the topic is deleted
    - delete orphan sections removed from this collection

    This guarantees that a section can never exist without
    its parent topic.
    """

    # ==========================================================
    # AUDIT
    # ==========================================================

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        nullable=False,
        description="Timestamp when the topic was created.",
    )

    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        nullable=False,
        description="Timestamp when the topic metadata was last updated.",
    )