from pydantic import BaseModel

class SectionDTO(BaseModel):
    """
    Inner section extracted from a bookmark.
    """

    bookmark_title: str
    title: str

    start_page: int
    end_page: int  # ✅ ADD THIS (important)

    next_section_title: str | None = None
    next_bookmark_title: str | None = None
