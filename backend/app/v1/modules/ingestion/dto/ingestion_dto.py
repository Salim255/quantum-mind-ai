from pydantic import BaseModel, Field


class IngestionResponseDto(BaseModel):
    """
    Response returned after ingesting a document into the vector store.
    """

    status: str = Field(..., description="Ingestion status (ok / failed)")
    chunks_added: int = Field(..., description="Number of chunks successfully stored")
    source: str = Field(..., description="Source of the ingested document")