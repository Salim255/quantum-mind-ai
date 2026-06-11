from pydantic import BaseModel

from typing import Literal
from pydantic import BaseModel


class ContentBlockDTO(BaseModel):
    """
    Unified content unit inside a section.
    """

    bookmark_title: str
    section_title: str

    type: Literal["text", "figure", "equation", "circuit"]

    order: int

    content: str | None = None

    image_path: str | None = None

    caption: str | None = None
    
class TextDTO(BaseModel):
    """
    Extracted text belonging to a section.
    """

    bookmark_title: str

    section_title: str

    content: str