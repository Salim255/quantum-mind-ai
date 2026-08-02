from abc import ABC, abstractmethod

class TopicService(ABC):
    @abstractmethod
    def get_topic_with_sections_and_blocks(topic_id: int):
        # Instead of silently doing nothing (pass), it raises:
        raise NotImplementedError("get_topic_with_sections_and_blocks() must be implemented in a subclass")