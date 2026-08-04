import logging
from uuid import UUID
from app.repositories.topic_repository import TopicRepository
from app.v1.modules.topic.service.topic_service import TopicService
from app.v1.modules.topic.dto.topic_create_dto import TopicCreateDTO
from app.v1.modules.topic.dto.topic_dto import TopicDTO
from app.v1.modules.topic.dto.topic_update_dto import TopicUpdateDTO
from app.models.topic import Topic
from app.v1.modules.topic.dto.topics_reponse_dto import TopicsResponseDTO
from app.v1.modules.topic.dto.topic_with_sections_dto import TopicWithSectionsDTO


logger = logging.getLogger(__name__)

class TopicImplService(TopicService):
    def __init__(self, topic_repository: TopicRepository):
        self.topic_repository = topic_repository

    async def create_topic(self, topic_data: TopicCreateDTO) -> TopicDTO:
        try:
            topic = Topic(
                **topic_data.model_dump()
            )
            await self.topic_repository.add(topic)
            
            return TopicDTO.model_validate(topic)
        except Exception as e:
            # Log the exception for debugging purposes
            logger.exception(f"Error creating topic: {e}")
            raise e


    async def get_topic(self, topic_id: UUID):
        topic: Topic  =  self.topic_repository.get_by_id(topic_id)

        if topic is None:
            return None
        
        return TopicDTO.model_validate(topic)
    

    async def get_topics(self) -> TopicsResponseDTO:
        topics = self.topic_repository.list()

        return TopicsResponseDTO(
            topics=[TopicDTO.model_validate(topic) for topic in topics]
        )

    async def get_topics_with_sections_and_blocks(self)-> list[TopicWithSectionsDTO] :
       try:
            topics = await self.topic_repository.get_topics_with_sections_with_blocks()

            if topics is None:
                return []

            return [
                TopicWithSectionsDTO.model_validate(topic).model_dump()
                for topic in topics
            ]
       
       except Exception as e:
            # Log the exception for debugging purposes
            logger.exception(f"Error retrieving topics with sections and blocks: {e}")
            raise e

    async def get_topic_with_sections(self, topic_id: UUID):
        topic = self.topic_repository.get_by_id(topic_id)
        if topic is None:
            return None
        return TopicDTO.model_validate(topic)

    async def get_topic_with_sections_and_blocks(self, topic_id: UUID):
        topic = await self.topic_repository.get_by_id(topic_id)
        if topic is None:
            return None
        return TopicDTO.model_validate(topic)


    async def update_topic(self, topic_id: UUID, topic_data: TopicUpdateDTO):
        topic = self.topic_repository.get_by_id(topic_id)
        if topic is None:
            return None
        for key, value in topic_data.model_dump().items():
            setattr(topic, key, value)
 
        return TopicDTO.model_validate(topic)

    async def delete_topic(self, topic_id: UUID):
        topic = self.topic_repository.get_by_id(topic_id)
        if topic is None:
            return None
        
        self.topic_repository.delete(topic)
    
        return TopicDTO.model_validate(topic)