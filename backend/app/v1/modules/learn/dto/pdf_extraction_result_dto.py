from pydantic import BaseModel

from app.v1.modules.learn.dto.bookmark_dto import BookmarkDTO
from app.v1.modules.learn.dto.section_dto import SectionDTO
from app.v1.modules.learn.dto.text_dto import TextDTO
from app.v1.modules.learn.dto.image_dto import ImageDTO
from app.v1.modules.learn.dto.equation_dto import EquationDTO


class PdfExtractionResultDTO(BaseModel):
    """
    Fully structured PDF extraction output.
    """

    bookmarks: list[BookmarkDTO]

    sections: list[SectionDTO]

    texts: list[TextDTO]

    images: list[ImageDTO]

    equations: list[EquationDTO]