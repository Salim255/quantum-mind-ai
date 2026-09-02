import logging
from uuid import UUID
from app.repositories.topic_repository import TopicRepository
from app.v1.modules.topic.service.topic_service import TopicService
from app.v1.modules.topic.dto.topic_create_dto import TopicCreateDTO
from app.v1.modules.topic.dto.topic_dto import TopicDTO, TopicOnlyDTO
from app.v1.modules.topic.dto.topic_update_dto import TopicUpdateDTO
from app.models.topic import Topic
from app.v1.modules.topic.dto.topics_response_dto import TopicsResponseDTO
from app.v1.modules.topic.dto.topic_with_sections_dto import TopicWithSectionsDTO
from app.v1.modules.topic.dto.topics_with_sections_response_dto import TopicsWithSectionsResponseDTO

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
        try:
            topic: Topic  =  self.topic_repository.get_by_id(topic_id)
            
            if topic is None:
                return None
            
            return TopicDTO.model_validate(topic)
        except Exception as e:
            logger.exception(f"Error in get topic {e}")
            raise
    
    
    #### 
    # ==========================================================
    # GET TOPICS
    # ==========================================================

    async def get_topics(
        self,
        include_sections: bool = True,
        include_blocks: bool = True,
    ) -> TopicsResponseDTO | TopicsWithSectionsResponseDTO:
        """
        Retrieve learning topics with an optional level of nested content.

        The method acts as the main entry point for topic retrieval and
        delegates the actual retrieval/transformation to the appropriate
        helper based on the requested includes.

        Supported combinations:

        - topics only
        - topics + sections
        - topics + blocks
        - topics + sections + blocks
        """

        try:
            # ------------------------------------------------------
            # Topics + sections + blocks
            # ------------------------------------------------------
            if include_sections and include_blocks:
                return await self.get_topics_with_sections_and_blocks()


            # ------------------------------------------------------
            # Topics only
            # ------------------------------------------------------
            return await self._get_topics_only()

        except Exception as e:
            logger.exception(
                f"Error retrieving topics: {e}"
            )
            raise


    # ==========================================================
    # GET TOPICS ONLY
    # ==========================================================

    async def _get_topics_only(
        self,
    ) -> TopicsResponseDTO:
        """
        Retrieve topics without any nested sections or blocks.
        """

        topics = await self.topic_repository.get_all()
     
        return TopicsResponseDTO(
            topics=[
                TopicOnlyDTO.model_validate(topic)
                for topic in topics
            ]
        )



    # ==========================================================
    # GET TOPICS WITH SECTIONS AND BLOCKS
    # ==========================================================

    async def get_topics_with_sections_and_blocks(
        self,
    ) -> TopicsWithSectionsResponseDTO:
        """
        Retrieve topics with their complete learning hierarchy.

        Structure:

        Topic
        ├── Topic Blocks
        └── Sections
            └── Section Blocks
        """

        topics = (
            await self.topic_repository
            .get_topics_with_sections_with_blocks()
        )

        if topics is None:
            return TopicsWithSectionsResponseDTO(
                topics=[]
            )

        return TopicsWithSectionsResponseDTO(
            topics=[
                TopicWithSectionsDTO.model_validate(topic).model_dump()
                for topic in topics
            ]
        )


    async def get_topic_with_sections(self, topic_id: UUID):
        try:
            topic = self.topic_repository.get_by_id(topic_id)

            if topic is None:
                return None
            
            return TopicDTO.model_validate(topic)
        
        except Exception as e:
            logger.exception(f"Error in get topic with sections: {e}")

            raise

    async def get_topic_with_sections_and_blocks(self, topic_id: UUID):
        try:

            topic = await self.topic_repository.get_by_id(topic_id)
            if topic is None:
                return None
            return TopicDTO.model_validate(topic)
        
        except Exception as e:
            print(f"Error in get topic with sections and blocks: {e}")
            raise


    async def update_topic(self, topic_id: UUID, topic_data: TopicUpdateDTO):
       try:
            
            topic = self.topic_repository.get_by_id(topic_id)

            if topic is None:
                return None
            
            for key, value in topic_data.model_dump().items():
                setattr(topic, key, value)
    
            return TopicDTO.model_validate(topic)
       
       except Exception as e:
           logger.exception(f"Error in update topic: {e}")
           raise

    async def delete_topic(self, topic_id: UUID):
       try:
            
            topic = self.topic_repository.get_by_id(topic_id)

            if topic is None:
                return None
            
            self.topic_repository.delete(topic)
        
            return TopicDTO.model_validate(topic)
       
       except Exception as e:
            logger.exception(f"Error in delete topic {e}")

            raise