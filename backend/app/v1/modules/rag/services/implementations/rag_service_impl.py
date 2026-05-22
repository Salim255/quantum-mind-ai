import time
from typing import Annotated, List
from fastapi import Depends
from pydantic import BaseModel
from app.ai_core.llms.groq_llm import get_groq_client
from app.v1.modules.rag.context.context_builder import build_context
from app.ai_core.structured_outputs.schemas.rag_response_schema import RAGQueryResponseSchema
from app.v1.modules.rag.services.interfaces.rag_service import RAGService
from app.v1.modules.rag.generator.generator_service import generate_answer
from app.v1.modules.rag.retriever.retriever import retrieve
from app.core.settings import Settings
from app.ai_core.structured_outputs.schemas.rag_eval_schema import RAGEvaluationLog
from app.v1.modules.rag.evaluation.logger import log_rag_evaluation
from app.v1.modules.rag.dto.retrieval_dto import (RetrievalResponseDTO, RetrievalChunkDTO)

class QueryRequest(BaseModel):
    query: str
    top_k: int = 3

class RAGServiceImpl(RAGService):
   def __init__(self, settings: Settings):
        self.settings = settings
        
   def rag_pipeline(
         self,
         payload: QueryRequest
         ) -> RAGQueryResponseSchema:
    """
    Execute the full RAG pipeline.

    INPUT
    -----
    payload.query:
        User question

    payload.top_k:
        Number of chunks to retrieve

    OUTPUT
    ------
    - query
    - retrieved chunks
    - structured final answer
    - sources
    - latency
    """

    # ---------------------------------------------------------------
    # START LATENCY TIMER
    # ---------------------------------------------------------------
    #
    # We measure total pipeline execution time.
    #
    # Useful later for:
    # - monitoring
    # - dashboard analytics
    # - optimization
    # - performance regression detection
    # ---------------------------------------------------------------
    start_time = time.perf_counter()
    # ---------------------------------------------------------------
    # 1. SEMANTIC RETRIEVAL + RERANKING
    # ---------------------------------------------------------------
    #
    # search_similar_documents():
    #
    # - embeds the query
    # - performs cosine similarity search
    # - selects top candidates
    # - reranks using cross-encoder
    #
    # RETURNS:
    # {
    #   "results": [...],
    #   "sources": [...]
    # }
    # ---------------------------------------------------------------
        
    retrieval_output: RetrievalResponseDTO = retrieve(payload.query)

    # ---------------------------------------------------------------
    # EXTRACT RETRIEVED CHUNKS
    # ---------------------------------------------------------------
    chunks: List[RetrievalChunkDTO] = retrieval_output.results  # List of text chunks relevant to the query

    # ---------------------------------------------------------------
    # LOW CONFIDENCE RETRIEVAL GUARD
    # ---------------------------------------------------------------
    # If retrieval found no reliable chunks,
    # avoid hallucinated generation.
    # ---------------------------------------------------------------
    # Final answer (must be grounded in context)

    if not chunks:
        return RAGQueryResponseSchema(
            query=payload.query,
            retrieved_chunks=[],
            final_answer={
                "answer": (
                    "I could not find reliable information "
                    "to answer this question."
                ),
                "key_points": [],
                "step_by_step": [],
                "sources": [],
                "retrieved_chunk":[]
            },
            latency_ms=0
        )

    # ---------------------------------------------------------------
    # 2. BUILD OPTIMIZED CONTEXT
    # ---------------------------------------------------------------
    #
    # build_context():
    #
    # - merges top chunks
    # - limits total context size
    # - preserves semantic coherence
    #
    # WHY IMPORTANT?
    # --------------
    # LLMs perform better with:
    # - focused context
    # - low noise
    # - coherent passages
    # ---------------------------------------------------------------
    rich_context_chunks = build_context(
        chunks,
        max_chars=3000
    )

    # ---------------------------------------------------------------
    # 3. INITIALIZE LLM CLIENT
    # ---------------------------------------------------------------
    #
    # This creates the Groq client using API keys
    # from application settings.
    # ---------------------------------------------------------------
    client = get_groq_client(self.settings)

    # ---------------------------------------------------------------
    # 4. GENERATE FINAL STRUCTURED ANSWER
    # ---------------------------------------------------------------
    #
    # generate_answer():
    #
    # - builds the final RAG prompt
    # - injects context
    # - calls the LLM
    # - validates structured JSON output
    #
    # RETURNS:
    # RAGResponseSchema
    # ---------------------------------------------------------------

    final_answer =  generate_answer(
        payload.query,
        rich_context_chunks,
        client
    )

    # ---------------------------------------------------------------
    # STOP LATENCY TIMER
    # ---------------------------------------------------------------
    #
    # Convert total execution time into milliseconds.
    # ---------------------------------------------------------------
    latency_ms = (
        time.perf_counter() - start_time
    ) * 1000

  
    # ---------------------------------------------------------------
    # 6. CREATE RAG EVALUATION LOG
    # ---------------------------------------------------------------
    #
    # This stores:
    # - query
    # - retrieved chunks
    # - final answer
    # - latency
    # - model info
    #
    # This becomes the foundation of:
    # - RAG analytics
    # - evaluation dashboards
    # - retrieval benchmarking
    # ---------------------------------------------------------------
    evaluation_log = RAGEvaluationLog(
        query=payload.query,
        retrieved_chunks=chunks,
        final_answer=final_answer.model_dump(),
        latency_ms=latency_ms,
        model="llama-3.1-8b-instant",
        top_k=payload.top_k
    )

    # ---------------------------------------------------------------
    # 7. SAVE EVALUATION LOG
    # ---------------------------------------------------------------
    #
    # Logs are stored in JSONL format.
    #
    # Every request becomes:
    # - traceable
    # - measurable
    # - debuggable
    # ---------------------------------------------------------------
    log_rag_evaluation(evaluation_log)

    # ---------------------------------------------------------------
    # 8. RETURN API RESPONSE
    # ---------------------------------------------------------------
    #
    # model_dump():
    # Converts Pydantic schema into JSON-serializable dict.
    # ---------------------------------------------------------------
    return RAGQueryResponseSchema(
        query=payload.query,
        retrieved_chunks=chunks,
        final_answer=final_answer,
        latency_ms=latency_ms
    )
   
   