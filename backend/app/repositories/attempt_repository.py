from app.repositories.base_repository import BaseRepository
from app.models.attempt import Attempt
from app.models.question import Question
from app.models.topic import Topic
from sqlalchemy.orm import selectinload
from sqlmodel import Session, select
from uuid import UUID


class AttemptRepository(BaseRepository[Attempt]):
    """
    Repository for quiz_attempts database queries.

    Inherits common CRUD operations from BaseRepository.
    """
     
    def __init__(self, session: Session):
        super().__init__(session, Attempt)


           
    async def get_by_id_with_topic(
        self,
        attempt_id: UUID,
    ) -> Attempt | None:
        """
        Retrieve an attempt together with its associated topic.

        This method explicitly loads the topic to prevent lazy-loading
        database operations during asynchronous DTO serialization.

        Args:
            attempt_id:
                Identifier of the attempt.

        Returns:
            The attempt with its topic loaded, or None if not found.
        """
        statement = (
                select(Attempt)
                .options(
                    selectinload(Attempt.topic),
                )
                .where(
                    Attempt.id == attempt_id,
                )
            )

        result = await self.session.execute(statement)

        return result.scalar_one_or_none()
    
    # ============================================================
    # ATTEMPT + TOPIC + QUESTIONS + ANSWERS
    # ============================================================

    async def get_by_id_with_topic_questions(
        self,
        attempt_id: UUID,
    ) -> Attempt | None:
        """
        Retrieve an attempt with its complete learning content.

        The returned object contains:

            Attempt
                └── Topic
                     └── Questions
                          └── Answers

        Questions are loaded through the attempt's topic and their
        answer options are loaded together with each question.

        This query is intended for starting or resuming a quiz,
        where the client needs all questions and their available
        answer options.

        Args:
            attempt_id:
                Identifier of the attempt.

        Returns:
            The attempt with topic, questions, and answers loaded,
            or None if the attempt does not exist.
        """
        statement = (
            select(Attempt)
            .options(
                selectinload(
                    Attempt.topic
                )
                .selectinload(
                    Topic.questions
                )
                .selectinload(
                    Question.answers
                ),
            )
            .where(
                Attempt.id == attempt_id,
            )
        )

        result = await self.session.execute(statement)

        return result.scalar_one_or_none()