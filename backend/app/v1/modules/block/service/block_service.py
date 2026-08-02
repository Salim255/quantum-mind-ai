
from abc import ABC

class BlockService(ABC):
    """
    Implementation of the BlockService interface.
    This class provides the actual business logic for managing blocks.
    It interacts with the BlockRepository to perform CRUD operations and other business-related tasks.
    """

    async def create_block(self, block_data):
        """
        Creates a new block.

        Example:

            Block 1
            Block 2
            Block 3

        Returns:
            The created Block entity.
        """
        raise NotImplementedError(
            "create_block() must be implemented"
        )   