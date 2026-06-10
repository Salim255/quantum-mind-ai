from pydantic import BaseModel

class SectionDTO(BaseModel):
    """
    Inner section extracted from a bookmark.
    """

    bookmark_title: str

    title: str

    start_page: int

    next_section_title: str | None = None

    next_section_page: int | None = None

    next_bookmark_title: str | None = None
