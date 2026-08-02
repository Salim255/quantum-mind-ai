from datetime import datetime, UTC
from uuid import UUID, uuid4
from sqlmodel import Field, Relationship, SQLModel
from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import JSONB
from app.v1.modules.block.dto.block_type_dto import BlockTypeDTO


class Block(SQLModel, table=True):
    """
    Represents the smallest educational unit inside a QuantumMind lesson.

    A Block is the atomic piece of learning content rendered by the frontend.

    Blocks allow lessons to be composed dynamically from different
    educational elements without changing the database schema.

    Supported examples include:

    - Heading
    - Paragraph
    - Ordered List
    - Unordered List
    - Equation
    - Image
    - Code
    - Example
    - Exercise
    - Interactive Component

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

            4. Ordered List
                - Vector has a dimension
                - Vector contains entries

            5. Example
                "Three-dimensional ket"

    A Block stores only:

    - ownership
    - rendering type
    - rendering payload
    - ordering
    - publication state

    The frontend is responsible for rendering each block
    according to its type.
    """

    __tablename__ = "blocks"

    # ==========================================================
    # IDENTITY
    # ==========================================================

    id: UUID = Field(
        default_factory=uuid4,
        primary_key=True,
        index=True,
        description="Unique identifier of the learning block.",
    )

    # ==========================================================
    # PARENT RELATIONSHIP
    # ==========================================================

    topic_id: UUID | None = Field(
        default=None,
        foreign_key="topics.id",
        index=True
    )

    topic: "Topic" = Relationship(
    back_populates="blocks"
)
    """
    Parent learning topic containing this block.
    """
    
    section_id: UUID | None = Field(
        foreign_key="sections.id",
        default=None,
        index=True,
        description=(
            "Identifier of the parent section that owns this block."
        ),
    )

    section: "Section" = Relationship(
        back_populates="blocks",
    )
    """
    Parent learning section containing this block.

    Relationship:

        Section
            └── Blocks

    Every block belongs to exactly one section.
    """

    # ==========================================================
    # BLOCK DEFINITION
    # ==========================================================

    type: BlockTypeDTO = Field(
        nullable=False,
        index=True,
        description=(
            "Rendering type of the block."
        ),
    )

    content: dict = Field(
        sa_column=Column(
            JSONB,
            nullable=False,
            default=dict,
        ),
        description=(
            "Structured payload required to render this block."

            "Its structure depends entirely on the block type."

            "Examples:"

            "- paragraph → text"

            "- equation → latex"

            "- image → image url"

            "- list → array of items"

            "- exercise → question and answers"
        ),
    )

    # ==========================================================
    # ORGANIZATION
    # ==========================================================

    display_order: int = Field(
        default=0,
        nullable=False,
        description=(
            "Display order of the block inside its parent section."
        ),
    )

    # ==========================================================
    # PUBLICATION
    # ==========================================================

    is_published: bool = Field(
        default=True,
        nullable=False,
        description=(
            "Indicates whether this block is visible to learners."
        ),
    )

    # ==========================================================
    # AUDIT
    # ==========================================================

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        nullable=False,
        description="Timestamp when the block was created.",
    )

    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        nullable=False,
        description="Timestamp when the block was last modified.",
    )