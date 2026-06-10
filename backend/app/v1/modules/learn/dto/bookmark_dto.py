from pydantic import BaseModel


class BookmarkDTO(BaseModel):
    """
    Top-level bookmark extracted from PDF.
    """

    title: str
    order: int
    start_page: int
    end_page: int
