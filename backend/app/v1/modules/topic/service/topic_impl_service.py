from app.repositories.topic_repository import TopicRepository
from app.repositories.section_repository import SectionRepository
from app.repositories.block_repository import BlockRepository
from app.models.topic import Topic
from app.models.section import Section
from app.models.block import Block
from app.v1.modules.topic.service.topic_service import TopicService

class TopicImplService(TopicService):
    def __init__(self, topic_repository, section_repository, block_repository):
        self.topic_repository = topic_repository
        self.section_repository = section_repository
        self.block_repository = block_repository

    def get_topic_with_sections_and_blocks(self, topic_id: int):
        # Fetch the topic
        topic = self.topic_repository.get_by_id(topic_id)
        if not topic:
            return None

        # Fetch sections related to the topic
        sections = self.section_repository.get_by_topic_id(topic_id)

        # For each section, fetch its blocks
        for section in sections:
            blocks = self.block_repository.get_by_section_id(section.id)
            section.blocks = blocks  # Assuming Section model has a 'blocks' attribute

        # Attach sections to the topic
        topic.sections = sections  # Assuming Topic model has a 'sections' attribute

        return topic