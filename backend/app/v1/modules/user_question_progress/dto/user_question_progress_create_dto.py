from uuid import UUID

from pydantic import BaseModel, ConfigDict


class UserQuestionProgressCreateDTO(BaseModel):
    """
    DTO used to initialize progress tracking for a user and question.

    Progress metrics are intentionally not exposed here because
    they are initialized by the domain model and updated through
    learning interactions.
    """

    model_config = ConfigDict(
        from_attributes=True,
    )

    user_id: UUID

    question_id: UUID