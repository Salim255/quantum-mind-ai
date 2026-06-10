from pydantic import BaseModel
from app.v1.modules.learn.dto.section_dto import SectionDTO
class BookmarkDTO(BaseModel):
    """
    Top-level bookmark extracted from PDF.
    """

    title: str
    order: int
    start_page: int
    end_page: int

