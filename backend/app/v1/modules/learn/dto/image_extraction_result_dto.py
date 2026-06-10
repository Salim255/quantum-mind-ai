from pydantic import BaseModel

from app.v1.modules.learn.dto.image_dto import ImageDTO


class ImageExtractionResultDTO(BaseModel):
    images: list[ImageDTO]