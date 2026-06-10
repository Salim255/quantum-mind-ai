from pydantic import BaseModel

from app.v1.modules.learn.dto.bookmark_dto import BookmarkDTO
from app.v1.modules.learn.dto.section_dto import SectionDTO


class BookmarkExtractionResultDTO(BaseModel):
    """
    Full bookmark tree extracted from PDF.
    """

    bookmarks: list[BookmarkDTO]

    sections: list[SectionDTO]