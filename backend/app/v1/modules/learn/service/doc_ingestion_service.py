from abc import ABC, abstractmethod

class DocIngestionService(ABC):
    @abstractmethod
    def bookmarks_extraction(self):
        pass

    @abstractmethod
    def section_extraction(self):
        pass
    @abstractmethod
    def text_extraction(self):
        pass

    @abstractmethod 
    def image_extraction(self):
        pass