from typing import List
from app.v1.modules.rag.dto.retrieval_dto import RetrievalChunkDTO
from app.v1.modules.rag.context.context_builder import assign_context_role

class ContextRoleService:
    @staticmethod
    def assign_reasoning_roles(chunks: List[RetrievalChunkDTO])-> None:
        """
        Assign reasoning roles to retrieved chunks.

        Example roles:
        --------------
        - core
        - supporting
        - example

        WHY IMPORTANT?
        --------------
        Ordered reasoning context improves:
        - answer coherence
        - explanation quality
        - logical grounding
        """
   
        for index, chunk in enumerate(chunks):

            chunk.context_role = assign_context_role(
                chunk,
                index
            )