from abc import ABC, abstractmethod

class DocIngestionService(ABC):
    @abstractmethod
    def text_extraction(self):
        pass

    @abstractmethod 
    def image_extraction(self):
        pass