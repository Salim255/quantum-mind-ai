from pydantic import BaseModel

from app.v1.modules.topic.dto.topic_dto import TopicDTO
from app.v1.modules.attempt.dto.attempt_dto import AttemptDTO


class ExploreQuizDTO(BaseModel):
    """
    Represents one quiz displayed in the Explore page.

    The topic contains the quiz's public information.

    The latest_attempt contains the current user's latest attempt
    for this topic, when one exists.

    If the user has never attempted the topic, latest_attempt is None.
    """

    topic: TopicDTO

    latest_attempt: AttemptDTO | None = None


class ExploreQuizzesResponseDTO(BaseModel):
    """
    Response containing the quizzes available in Explore.

    Each quiz contains:
    - the topic information
    - the current user's latest attempt, if one exists
    """

    quizzes: list[ExploreQuizDTO]