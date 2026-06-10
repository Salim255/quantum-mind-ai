from pydantic import BaseModel

class SectionTextDTO(BaseModel):
    """
    Extracted text belonging to a section.
    """

    bookmark_title: str

    section_title: str

    content: str