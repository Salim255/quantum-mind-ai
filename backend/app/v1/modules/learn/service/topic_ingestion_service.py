from abc import ABC, abstractmethod

class TopicIngestionService(ABC):

    @abstractmethod
    def create_topic_from_pdf(self):
        pass 