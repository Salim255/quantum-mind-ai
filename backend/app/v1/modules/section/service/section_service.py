from abc import ABC, abstractmethod

from backend.app.v1.modules.ingestion.dto.section_dto import SectionDTO
from backend.app.v1.modules.section.dto.section_create_dto import SectionCreateDTO

class SectionService(ABC):
    """
    Defines the contract for Section business operations.

    A Section represents a sub-topic or a specific area of study
    within a broader learning topic in QuantumMind.

    Responsibilities:

        - Create learning sections
        - Retrieve sections
        - Update section information
        - Remove sections
        - Load section learning hierarchy

    The service does not handle:
        - database queries
        - SQL operations
        - HTTP concerns

    Those responsibilities belong to:
        Repository layer
        Controller/API layer
    """

    @abstractmethod
    async def create_section(
        self,
        section_data: SectionCreateDTO,
    ) -> SectionDTO:
        """
        Creates a new learning section.

        Example:

            Linear Algebra
            Quantum Entanglement
            Quantum Gates

        Returns:
            The created Section entity.
        """

        raise NotImplementedError(
            "create_section() must be implemented"
        )