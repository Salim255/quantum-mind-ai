from pydantic import BaseModel
from .attempt_dto import AttemptDTO

class AttemptResponseDTO(BaseModel):
    """
    Response containing an attempt, when one exists.
    """

    attempt: AttemptDTO | None = None