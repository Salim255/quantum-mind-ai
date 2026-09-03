from sqlmodel.ext.asyncio.session import AsyncSession
from app.core.container import Container

from app.v1.modules.explore.services.explore_service import ExploreService
from app.v1.modules.explore.services.explore_impl_service import ExploreImplService
from app.v1.modules.topic.service.topic_service import TopicService
from app.v1.modules.attempt.services.attempt_service import AttemptService
from app.v1.modules.topic.dependencies import get_topic_service
from app.v1.modules.attempt.dependencies import get_attempt_service

def get_explore_service(
    session: AsyncSession,
    container: Container,
)->ExploreService:

    topic_service: TopicService = get_topic_service(session=session, container=container)
    attempt_service: AttemptService = get_attempt_service(session=session, container=container)

    return ExploreImplService(
        attempt_service=topic_service,
        attempt_service=attempt_service
    )