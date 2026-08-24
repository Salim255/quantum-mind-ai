from app.repositories.base_repository import BaseRepository
from app.models.question import Question
from sqlmodel import Session
from uuid import UUID
from sqlmodel import select
from sqlalchemy import func

class QuestionRepository(BaseRepository[Question]):
    """
    Repository for question database queries.

    Inherits common CRUD operations from BaseRepository.
    """
    def __init__(self, session: Session):
        super().__init__(session, Question)


    # ============================================================
    # QUESTION COUNT
    # ============================================================
    async def count_by_topic_id(
        self,
        topic_id: UUID,
    ) -> int:
        """
        Count the active questions belonging to a specific topic.

        This method is used by the QuestionService when another
        part of the application needs to know how many questions
        are available for a learning topic.

        Only active questions are counted, ensuring that disabled
        questions are not included when creating a quiz attempt.

        Args:
            topic_id:
                Identifier of the topic whose questions
                should be counted.

        Returns:
            The total number of active questions belonging
            to the specified topic.
        """

        statement = (
            select(func.count())
            .select_from(Question)
            .where(
                Question.topic_id == topic_id,
                Question.is_active.is_(True),
            )
        )

        result = await self.session.execute(statement)

        return result.scalar_one()