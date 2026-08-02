from datetime import datetime, UTC
from uuid import UUID, uuid4

from sqlmodel import SQLModel, Field


class Topic(SQLModel, table=True):
    """
    Represents a top-level learning topic inside QuantumMind.

    A topic is the entry point of a learning resource.
    It provides the information needed to display a topic card,
    create navigation routes, organize learning categories,
    and connect users with the actual educational content.

    A topic DOES NOT store lesson content.

    Detailed educational material is stored separately through:

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
        description="Unique identifier of the learning topic."
    )


    # ==========================================================
    # DISPLAY INFORMATION
    # ==========================================================

    title: str = Field(
        max_length=255,
        nullable=False,
        index=True,
        description=(
            "Human-readable title displayed to users. "
            "Example: 'Quantum Entanglement'."
        )
    )


    slug: str = Field(
        max_length=255,
        nullable=False,
        unique=True,
        index=True,
        description=(
            "URL-friendly identifier used for routing and public links. "
            "Example: 'quantum-entanglement'. "
            "Should remain stable even if the title changes."
        )
    )


    description: str | None = Field(
        default=None,
        nullable=True,
        description=(
            "Short introduction displayed before entering the topic. "
            "Used for topic cards, previews, and summaries. "
            "Does not contain the full lesson content."
        )
    )


    # ==========================================================
    # ORGANIZATION
    # ==========================================================

    category: str = Field(
        max_length=100,
        nullable=False,
        index=True,
        description=(
            "High-level grouping used to organize topics. "
            "Example: 'Quantum Physics', 'Mathematics', 'Programming'."
        )
    )


    order: int = Field(
        default=0,
        nullable=False,
        description=(
            "Controls the display order of topics inside a category "
            "or learning path."
        )
    )


    # ==========================================================
    # AUDIT
    # ==========================================================

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        nullable=False,
        description="Timestamp when the topic was created."
    )


    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        nullable=False,
        description="Timestamp when the topic metadata was last updated."
    )