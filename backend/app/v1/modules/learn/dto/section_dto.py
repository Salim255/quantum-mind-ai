from pydantic import BaseModel

class SectionDTO(BaseModel):
    """
    Inner section extracted from a bookmark.
    """

    bookmark_title: str

    title: str

    order: int

    start_page: int

    end_page: int