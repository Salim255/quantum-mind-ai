from fastapi import logger

from app.repositories.block_repository import BlockRepository
from app.v1.modules.block.service.block_service import BlockService
from app.v1.modules.block.service.block_service import BlockService
from app.models.block import Block

class BlockImplService(BlockService):
    """
    Implementation of the BlockService interface.
    This class provides the actual business logic for managing blocks.
    It interacts with the BlockRepository to perform CRUD operations and other business-related tasks.
    """

    def __init__(self, block_repository: BlockRepository):
        self.block_repository = block_repository

    # Implement the methods defined in BlockService here
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
        # Implement the logic to create a block using the block_repository
        try:
            block = Block(**block_data.model_dump())
            self.block_repository.add(block)
            return block
        except Exception as e:
            logger.error(f"Error creating block: {e}")
            raise e