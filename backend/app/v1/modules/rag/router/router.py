from fastapi import APIRouter, Depends, Depends
from typing import Annotated
from app.ai_core.structured_outputs.schemas.rag_response_schema import RAGQueryResponseSchema
from app.main import QueryRequest, get_settings
from app.core.settings import Settings
from app.main import QueryRequest
from app.ai_core.rag.services.interfaces.generator_service import GeneratorService
from app.ai_core.rag.services.interfaces.retriever_service import RetrieverService
from app.v1.modules.rag.dependencies import (get_answer_generator_service, get_retriever_service)

rag_router = APIRouter(
    prefix="/rag",
    tags=["RAG"]
)

@rag_router.post("/query")
def rag_query(
    payload: QueryRequest,
    settings: Annotated[Settings, Depends(get_settings)],
    retriever_service: Annotated[RetrieverService, Depends(get_retriever_service)],
    generator_service: Annotated[GeneratorService, Depends(get_answer_generator_service)]
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
    
    retrieval_output = retriever_service.retrieve(payload.query)

    # ---------------------------------------------------------------
    # EXTRACT RETRIEVED CHUNKS
    # ---------------------------------------------------------------
    chunks = retrieval_output.get("results", [])  # List of text chunks relevant to the query

    # ---------------------------------------------------------------
    # EXTRACT SOURCES
    # ---------------------------------------------------------------
    #
    # Sources help:
    # - explain provenance
    # - improve trust
    # - support evaluation
    # ---------------------------------------------------------------
    sources = retrieval_output.get("sources", [])  # List of sources corresponding to each chunk

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
    client = get_groq_client(settings)

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
   
    final_answer =  generator_service.generate_answer(
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
    # 5. BUILD STRUCTURED RETRIEVED CHUNKS
    # ---------------------------------------------------------------
    #
    # We transform raw chunks into structured objects
    # for evaluation logging.
    #
    # WHY?
    # ----
    # Later we can:
    # - inspect retrieval quality
    # - build dashboards
    # - compute metrics
    # - analyze hallucinations
    # ---------------------------------------------------------------
    retrieved_chunk_objects = []

    for chunk, source in zip(chunks, sources):

        retrieved_chunk_objects.append(

            RetrievedChunk(
                text=chunk,
                source=source
            )
        )

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

        retrieved_chunks=retrieved_chunk_objects,

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

        retrieved_chunks=rich_context_chunks,

        final_answer=final_answer,

        source=sources,

        latency_ms=latency_ms
    )