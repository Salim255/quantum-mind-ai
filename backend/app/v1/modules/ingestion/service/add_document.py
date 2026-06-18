# NumPy is used for handling vectors (embeddings).
# Even if this function does not manipulate vectors directly,
# NumPy is essential for similarity search later in the pipeline.
from uuid import uuid4
from app.v1.modules.rag.dto.chunk_dto import ChunkDTO
from app.v1.modules.rag.dto.document_dto import (DocumentDTO, AddedDocResponseDto, MetadataDTO)
from app.core.container import Container
from app.db.qdrant_mapper import QdrantMapper

# Import the embedding function.
# This function converts raw text into a dense vector representation
# that your QuantumMind AI system will use for retrieval.


# In-memory vector database.
# Each entry will look like:
# { "text": "...", "embedding": [0.12, -0.44, ...], "source": "lesson" }

class RAGAddDocument:
    def __init__(self, container: Container):
        self.container:Container = container
    
    async def add_qdrant_document(self, chunk: ChunkDTO, source: str = "document"):
        """
        Add a document to the QuantumMind AI vector store.

        Parameters
        ----------
        text : str
            The raw text content to store and embed.
            This can be a lesson, explanation, formula description,
            or any quantum learning material.

        source : str
            A tag describing the origin of the content.
            Helps the retriever prioritize and rank results.
            Defaults to "document".

        Returns
        -------
        dict
            A simple status dictionary confirming the operation.
        """

        # --- 1. Generate an embedding for the provided text ----------------------
        # The embed_text() tool returns a dictionary:
        # { "embedding": [...], "normalize": True, "source": "lesson" }
        # We extract only the vector because that's what we store in the DB.
        # 1. Extract text safely
        # text = chunk["text"] if isinstance(chunk, dict) else chunk
        embedding_result = self.container.rag_embedder.embed_text(text=chunk.text, source=source)
        emb = embedding_result["embedding"]


        # --- 2. Build the document entry ----------------------------------------
        document_entry = DocumentDTO(
            text=chunk.text,
            embedding=emb,
            metadata=MetadataDTO(
                source=source,
                concept=chunk.concept,
                length=chunk.length
            )
        )


        # --- 3. Save the entry in the in-memory vector DB -----------------------
        await self.container.qdrant.client.upsert(
            collection_name="documents",
            points=[
                QdrantMapper.to_point(
                    doc=document_entry,
                    point_id = str(uuid4())
                )
            ]
        )

        #self.container.qdrant.client.scroll(
        #    collection_name="documents",
        #    limit=1,
        #    with_vectors=True
        #)

    
        # --- 4. Return a confirmation -------------------------------------------
        # The agent_core expects a JSON-serializable response.
        return AddedDocResponseDto(
                status="ok",
                stored_text_length=len(chunk.text),
                source=source
            )