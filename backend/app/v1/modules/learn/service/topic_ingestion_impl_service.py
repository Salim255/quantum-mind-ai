from app.v1.modules.learn.service.topic_ingestion_service import TopicIngestionService
from app.v1.modules.learn.dto.create_topic_dto import CreateTopicsFromPdfDTO
from fastapi import UploadFile
from pypdf import PdfReader

class TopicIngestionImplService(TopicIngestionService):
    async def create_topic_from_pdf(self, file: UploadFile, topics: CreateTopicsFromPdfDTO):
        print("TOPICS=====", file.file)
        reader = PdfReader(file.file)
        print("Hello fom reade outlines====\n", reader.outline)

        # outlines = reader.outline
        return "Hello from create topic"