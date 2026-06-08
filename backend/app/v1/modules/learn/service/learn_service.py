from abc import ABC, abstractmethod
class LearnService(ABC):

    @abstractmethod
    def create_topic(self):
        pass