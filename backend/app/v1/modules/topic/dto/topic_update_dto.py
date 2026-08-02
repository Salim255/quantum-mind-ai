from pydantic import BaseModel, Field


class TopicUpdateDTO(BaseModel):
    """
    DTO used to update an existing QuantumMind learning topic.

    All fields are optional because updates can be partial.

    Example:

        Update only the title:

            {
                "title": "Advanced Quantum Entanglement"
            }

        Update only the description:

            {
                "description": "New learning introduction..."
            }
    """


    # ==========================================================
    # IDENTITY
    # ==========================================================

    title: str | None = Field(
        default=None,
        min_length=3,
        max_length=255,
        description=(
            "New human-readable title displayed to learners."
        )
    )


    slug: str | None = Field(
        default=None,
        min_length=3,
        max_length=255,
        description=(
            "New unique URL-friendly identifier."
        )
    )


    # ==========================================================
    # CLASSIFICATION
    # ==========================================================

    category: str | None = Field(
        default=None,
        max_length=100,
        description=(
            "New category used to organize the topic."
        )
    )


    # ==========================================================
    # PRESENTATION
    # ==========================================================

    description: str | None = Field(
        default=None,
        min_length=10,
        description=(
            "New short introduction displayed to learners."
        )
    )