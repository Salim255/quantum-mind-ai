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


class AttemptUpdateScoreResponseDTO(BaseModel):
    """
    Response returned after updating an attempt score.

    This DTO intentionally contains only attempt data.
    It does not include the topic or its questions.
    """

    id: UUID
    user_id: UUID |  None
    topic_id: UUID

    score: float
    total_questions: int
    correct_answers: int

    is_completed: bool