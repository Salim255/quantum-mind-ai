
from typing import Annotated

from fastapi import Depends, Request

from app.v1.modules.topic.service.topic_service import TopicService
from app.v1.modules.topic.service.topic_impl_service import TopicImplService
from app.repositories.topic_repository import TopicRepository
from app.core.container import Container

# ------------------------------------------------------------
# CONTAINER DEPENDENCY
# ------------------------------------------------------------
def get_container(request: Request) -> Container:
    return request.app.state.container

def get_topic_service(container: Annotated[Container, Depends(get_container)]) -> TopicService:
    topic_repository = TopicRepository()
    return TopicImplService(topic_repository, container=container)
