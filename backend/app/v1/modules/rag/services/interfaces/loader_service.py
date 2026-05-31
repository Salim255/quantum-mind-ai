from abc import ABC, abstractmethod
from app.v1.modules.rag.dto.ingestion_dto import IngestionResponseDto

class LoaderService(ABC):
    @abstractmethod
    async def upload_and_ingest_pdf(self, path: str, source: str) -> IngestionResponseDto:
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