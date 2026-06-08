from abc import ABC, abstractmethod

class LearnService(ABC):
    @abstractmethod
    def create_topic(self):
        pass

    @abstractmethod
    def update_topic(self):
        pass

    @abstractmethod
    def get_topics(self):
        pass