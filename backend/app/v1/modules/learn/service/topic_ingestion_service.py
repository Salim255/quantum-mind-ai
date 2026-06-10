from abc import ABC, abstractmethod
from app.v1.modules.learn.dto.create_topic_dto import CreateTopicsFromPdfDTO
from fastapi import UploadFile

class TopicIngestionService(ABC):
    @abstractmethod
    async def create_topic_from_pdf(self, file: UploadFile, topics: CreateTopicsFromPdfDTO):
        pass 