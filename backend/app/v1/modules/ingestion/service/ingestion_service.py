from abc import ABC, abstractmethod
from app.v1.modules.rag.dto.ingestion_dto import IngestionResponseDto
from fastapi import UploadFile

class IngestionService(ABC):
    @abstractmethod
    async def upload_and_ingest_pdf(self, file: UploadFile) -> IngestionResponseDto:
        """
        Abstract method to ingest a PDF into the system.

        Parameters
        ----------
        path : str
            The path to the PDF file.
        source : str
            The source of the PDF file.

        Returns
        -------
        IngestionResponseSchema
            The response indicating the outcome of the ingestion process.
        """
        pass