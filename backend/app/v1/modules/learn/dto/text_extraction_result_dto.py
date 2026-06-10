from pydantic import BaseModel

from app.v1.modules.learn.dto.text_dto import TextDTO


class TextExtractionResultDTO(BaseModel):
    texts: list[TextDTO]