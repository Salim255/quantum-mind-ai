
import logging

from app.v1.modules.section.service.section_service import SectionService
from app.v1.modules.ingestion.dto.section_dto import SectionDTO
from app.v1.modules.section.dto.section_create_dto import SectionCreateDTO
from app.models.section import Section
from app.repositories.section_repository import SectionRepository

logger = logging.getLogger(__name__)

class SectionImplService(SectionService):
    """
    Concrete implementation of the SectionService interface.

    This service provides the actual business logic for managing learning sections.
    It interacts with the repository layer to perform CRUD operations on Section entities.

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

    def __init__(self, section_repository: SectionRepository):
        """
        Initializes the SectionImplService with a section repository.

        Args:
            section_repository: An instance of SectionRepository for database operations.
        """
        self.section_repository = section_repository  


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

        try:
            # Here you would typically call the repository layer to persist the section_data
            # For example:
            # new_section = await self.section_repository.create(section_data)
            # return SectionDTO.from_orm(new_section)

            # Placeholder implementation for demonstration purposes
            new_section = Section(
                **section_data.model_dump()
            )

            await self.section_repository.add(new_section)

            return SectionDTO.model_validate(new_section)
        
        except Exception as e:
            # Handle exceptions and possibly log them
            logger.exception(f"Error creating section {e}")
            raise 