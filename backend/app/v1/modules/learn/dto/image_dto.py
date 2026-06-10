from pydantic import BaseModel


class ImageDTO(BaseModel):
    """
    Images extracted from PDF.
    """

    bookmark_title: str

    section_title: str

    image_path: str

    page_number: int