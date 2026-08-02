from abc import ABC

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