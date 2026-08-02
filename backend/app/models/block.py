from datetime import datetime, UTC
from uuid import UUID, uuid4

from sqlmodel import SQLModel, Field
from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import JSONB


class Block(SQLModel, table=True):
    """
    Represents a single educational content block inside a Section.

    A block is the smallest renderable unit of a QuantumMind lesson.

    Blocks allow a section to be composed dynamically from different
    educational elements:

        - heading
        - paragraph
        - ordered/unordered list
        - equation
        - image
        - example
        - exercise
        - code
        - interactive content


    Architecture:

        Topic
          |
          └── Section
                 |
                 └── Block


    Example:

        Section:
            "Vectors"

        Blocks:

            1. Heading
               "What is a vector?"

            2. Paragraph
               "A vector is a list of numbers..."

            3. Equation
               "|v| = √(x²+y²)"

            4. List
               - Vector has dimension
               - Vector has entries

            5. Example
               "Three dimensional ket"


    The Block table stores only:
        - ownership
        - type
        - ordering
        - content payload


    The frontend decides how each block type is rendered.
    """


    __tablename__ = "blocks"


    # ==========================================================
    # IDENTITY
    # ==========================================================

    id: UUID = Field(
        default_factory=uuid4,
        primary_key=True,
        index=True,
        description=(
            "Unique identifier of the content block."
        )
    )


    # ==========================================================
    # RELATIONSHIP
    # ==========================================================

    section_id: UUID = Field(
        foreign_key="sections.id",
        nullable=False,
        index=True,
        description=(
            "Reference to the parent section containing this block."
        )
    )


    # ==========================================================
    # BLOCK DEFINITION
    # ==========================================================

    type: str = Field(
        max_length=50,
        nullable=False,
        index=True,
        description=(
            "Defines how the frontend renders this block. "
            "Examples: paragraph, equation, list, image, example."
        )
    )


    content: dict = Field(
        sa_column=Column(JSONB),
        nullable=False,
        description=(
            "Stores the block-specific data required for rendering. "
            "The structure depends on the block type."
        )
    )


    # ==========================================================
    # ORDERING
    # ==========================================================

    order_index: int = Field(
        default=0,
        nullable=False,
        description=(
            "Controls the position of this block inside the section."
        )
    )


    # ==========================================================
    # VISIBILITY / STATE
    # ==========================================================

    is_published: bool = Field(
        default=True,
        nullable=False,
        description=(
            "Determines whether this block is visible to learners."
        )
    )


    # ==========================================================
    # AUDIT
    # ==========================================================

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        nullable=False,
        description=(
            "Timestamp when this block was created."
        )
    )


    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        nullable=False,
        description=(
            "Timestamp when this block was last modified."
        )
    )