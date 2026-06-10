from pydantic import BaseModel

class TextDTO(BaseModel):
    """
    Extracted text belonging to a section.
    """

    bookmark_title: str

    section_title: str

    content: str