from uuid import UUID

from pydantic import BaseModel


class AttemptUpdateScoreDTO(BaseModel):
    """
    Data required to evaluate an answer submitted
    for an existing learning attempt.

    The attempt identifies the assessment session,
    while the answer identifies the selected answer.
    """

    attempt_id: UUID
    answer_id: UUID