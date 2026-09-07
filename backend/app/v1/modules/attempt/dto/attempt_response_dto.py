from pydantic import BaseModel
from .attempt_dto import AttemptDTO
from .attempt_update_score_dto import AttemptUpdateScoreResponseDTO

class AttemptResponseDTO(BaseModel):
    """
    Response containing an attempt, when one exists.
    """

    attempt: AttemptDTO | AttemptUpdateScoreResponseDTO |  None = None