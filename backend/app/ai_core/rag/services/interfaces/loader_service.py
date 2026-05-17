from abc import ABC, abstractmethod
from app.ai_core.structured_outputs.schemas.ingestion_schema import IngestionResponseSchema

class LoaderService(ABC):
    @abstractmethod
    def ingest_pdf(self, path: str, source: str) -> IngestionResponseSchema:
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