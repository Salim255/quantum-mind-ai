import time
from typing import (List, Generator, AsyncGenerator)
from pydantic import BaseModel
from app.v1.modules.rag.context.context_builder import build_reasoned_context
from app.v1.modules.rag.dto.rag_finale_response_dto import RAGQueryFinaleResponseDto
from app.v1.modules.rag.services.interfaces.rag_service import RAGService
from app.v1.modules.rag.generator.generator_service import (generate_answer, generate_streaming_answer)
from app.v1.modules.rag.dto.rag_eval_dto import RAGEvaluationLogDto
from app.v1.modules.rag.evaluation.logger import log_rag_evaluation
from app.v1.modules.rag.dto.retrieval_dto import (RetrievalResponseDTO, RetrievalChunkDTO)
from app.v1.modules.rag.retriever.implementations.search_engine_impl import RetrieverImpl
from app.core.container import Container
from app.v1.modules.rag.retriever.services.spell_corrector_service import(SpellCorrectorService, SpellCorrectionResult)

class QueryRequest(BaseModel):
    query: str
    top_k: int = 3

class RAGServiceImpl(RAGService):
   def __init__(
        self,
        container: Container, 
        retriever_service: RetrieverImpl
        ):
        self.container = container
        self.retriever_service =  retriever_service

   async def rag_stream_pipeline(
        self,
        payload: QueryRequest
    ) -> AsyncGenerator[str, None]:
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
    # 1. SEMANTIC RETRIEVAL + RERANKING
    # ---------------------------------------------------------------
    #
    # search_similar_documents()
    # ---------------------------------------------------------------
    # Correct spell:words
    spell_correction_result:SpellCorrectionResult  =  SpellCorrectorService.correct(query=payload.query)

    print("Corrected corrected_query ===\n", spell_correction_result.corrected_query)
    
    retrieval_output: RetrievalResponseDTO = await self.retriever_service.search_similar_documents(
       spell_correction_result.corrected_query
       )

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
        message = (
                "I could not find enough relevant information to answer your question. "
                "Please ask a question related to quantum computing."
            )
        yield message
        return

    # ---------------------------------------------------------------
    # 2. BUILD OPTIMIZED CONTEXT
    # ---------------------------------------------------------------
    rich_context_chunks: str = build_reasoned_context(retrieval_output.results)


    # ---------------------------------------------------------------
    # 3. INITIALIZE LLM CLIENT
    # ---------------------------------------------------------------  
    client = self.container.groq_client
 
   
    # ---------------------------------------------------------------
    # 4. GENERATE FINAL STRUCTURED ANSWER
    # ---------------------------------------------------------------
    final_answer: Generator[str, None, None] = generate_streaming_answer(
        spell_correction_result.corrected_query,
        rich_context_chunks,
        client
    )

    # ---------------------------------------------------------------
    # 8. RETURN API RESPONSE
    # ---------------------------------------------------------------
    #
    # model_dump():
    # Converts Pydantic schema into JSON-serializable dict.
    # ---------------------------------------------------------------
    for chunk in final_answer:
       yield chunk
   
   def rag_pipeline(
        self,
        payload: QueryRequest
        ) -> RAGQueryFinaleResponseDto:
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
        
    retrieval_output: RetrievalResponseDTO = self.retriever_service.search_similar_documents(payload.query)

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
        return RAGQueryFinaleResponseDto(
            query=payload.query,
            retrieved_chunks=[],
            final_answer={
                "answer": (
                    "I could not find reliable information "
                    "to answer this question."
                ),
                "analogy": "",
                "confidence": 0.8
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
    #rich_context_chunks = build_context(
    #    chunks,
    #    max_chars=3000
    #)
    rich_context_chunks: str = build_reasoned_context(retrieval_output.results)


    # ---------------------------------------------------------------
    # 3. INITIALIZE LLM CLIENT
    # ---------------------------------------------------------------
    #
    # This creates the Groq client using API keys
    # from application settings.
    # ---------------------------------------------------------------
  
    client = self.container.groq_client
 
   
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
  
    final_answer = generate_answer(
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
    evaluation_log = RAGEvaluationLogDto(
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
    start = time.perf_counter()

    log_rag_evaluation(evaluation_log)

    print("log_rag_evaluation_timer___:\n",  time.perf_counter() - start)
    
    # ---------------------------------------------------------------
    # 8. RETURN API RESPONSE
    # ---------------------------------------------------------------
    #
    # model_dump():
    # Converts Pydantic schema into JSON-serializable dict.
    # ---------------------------------------------------------------
    return RAGQueryFinaleResponseDto(
        query=payload.query,
        retrieved_chunks=chunks,
        final_answer=final_answer,
        latency_ms=latency_ms
    )
   
   