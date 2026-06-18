from pydantic import BaseModel
from pydantic import BaseModel


class ContentBlockDTO(BaseModel):
    """
    Unified content unit inside a section.
    """

    bookmark_title: str
    section_title: str

    order: int

    content: str | None = None
