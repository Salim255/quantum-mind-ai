from pydantic import BaseModel, Field


class TopicCreateDTO(BaseModel):
    """
    DTO used to create a new QuantumMind learning topic.

    A topic represents a top-level educational resource.

    Example:

        Title:
            Quantum Entanglement

        Slug:
            quantum-entanglement

        Category:
            Quantum Physics

    Only client-provided data is accepted here.
    Database-generated fields such as id and timestamps
    are handled by the persistence layer.
    """


    # ==========================================================
    # IDENTITY
    # ==========================================================

    title: str = Field(
        min_length=3,
        max_length=255,
        description=(
            "Human-readable title displayed to learners."
        )
    )


    slug: str = Field(
        min_length=3,
        max_length=255,
        description=(
            "Unique URL-friendly identifier used for "
            "routing and public references."
        )
    )


    # ==========================================================
    # CLASSIFICATION
    # ==========================================================

    category: str = Field(
        max_length=100,
        description=(
            "Category used to organize learning topics."
            "Example: Quantum Physics, Mathematics."
        )
    )


    # ==========================================================
    # PRESENTATION
    # ==========================================================

    description: str = Field(
        min_length=10,
        description=(
            "Short introduction displayed before opening "
            "the complete learning content."
        )
    )

    display_order: int | None = Field(
        default=None,
        description=(
            "Controls the order of topics within a category. "
            "Lower numbers appear first in listings."
        )
    )