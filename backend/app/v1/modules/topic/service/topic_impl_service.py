from app.repositories.topic_repository import TopicRepository
from app.repositories.section_repository import SectionRepository
from app.repositories.block_repository import BlockRepository
from app.v1.modules.topic.service.topic_service import TopicService

class TopicImplService(TopicService):
    def __init__(self, topic_repository):
        self.topic_repository = topic_repository

    
    def create_topic(self, topic_data):
        return "hello from create_topic with topic_data: {topic_data}"

    def get_topic(self, topic_id: int):
        return "Topic details for topic_id: {topic_id}"

    def update_topic(self, topic_id: int, topic_data):
        return "Topic updated for topic_id: {topic_id} with topic_data: {topic_data}"
    
    def get_topic_with_sections_and_blocks(self, topic_id: int):
        return "Topic with sections and blocks for topic_id: {topic_id}"

    def delete_topic(self, topic_id: int):
        return "Topic deleted for topic_id: {topic_id}"