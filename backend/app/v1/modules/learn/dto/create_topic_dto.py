from pydantic import BaseModel, Field


class TopicDefinitionDTO(BaseModel):
    """
    Defines a single topic to be extracted from a PDF.
    """

    title: str = Field(
        min_length=3,
        max_length=255,
        description="Topic title displayed in the Learn section.",
    )

    category: str = Field(
        min_length=2,
        max_length=100,
        description="Topic category.",
    )

    start_page: int = Field(
        ge=1,
        description="First page belonging to this topic.",
    )

    end_page: int = Field(
        ge=1,
        description="Last page belonging to this topic.",
    )