from abc import ABC, abstractmethod

class IngestionService(ABC):
    @abstractmethod
    def ingest(self, data: dict) -> bool:
        """
        Abstract method to ingest data into the system.

        Parameters
        ----------
        data : dict
            The data to be ingested, which can include text, metadata, and other relevant information.

        Returns
        -------
        bool
            A boolean indicating whether the ingestion was successful or not.
        """
        pass