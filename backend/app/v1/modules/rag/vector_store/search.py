import numpy as np
from typing import List
from app.v1.modules.rag.embeddings.embedder import embed_text
from app.v1.modules.rag.vector_store.store import VECTOR_DB
from app.v1.modules.rag.retriever.reranker import rerank
from app.v1.modules.rag.dto.retrieval_dto import (RetrievalResponseDTO, RetrievalChunkDTO)
from app.v1.modules.rag.retriever.query_expander import expand_query

MIN_SIMILARITY_SCORE = 0.25
MIN_CONFIDENCE_SCORE = 1.5

def search_similar_documents(query: str, top_k: int = 3) -> RetrievalResponseDTO:
    """
    HYBRID SEMANTIC RETRIEVAL PIPELINE

    This function performs high-quality retrieval using:
    1. Dense embeddings (cosine similarity) → recall layer
    2. Cross-encoder reranker → precision layer
    3. Hybrid scoring → prevents losing strong matches

    WHY THIS DESIGN IS IMPORTANT
    ----------------------------
    - Cosine similarity ensures recall (finds relevant candidates)
    - Reranker ensures precision (reorders best answers)
    - Hybrid scoring prevents losing high-similarity matches
    """

    # ------------------------------------------------------------
    # 1. Embed query into vector space
    # ------------------------------------------------------------
    #q_emb = np.array(
    #    embed_text(text=query, source="user_query")["embedding"]
    #)

    expanded_queries = expand_query(query)
    query_embeddings = []
    for q in expanded_queries:
        emb = np.array(
            embed_text(
                text=q,
                source="user_query"
            )["embedding"]
        )
        query_embeddings.append(emb)
        
    scored = []

    print(f"[SEARCH] VECTOR_DB size: {len(VECTOR_DB)}")

    # ------------------------------------------------------------
    # 2. Compute cosine similarity against all documents
    # ------------------------------------------------------------
    for chunk in VECTOR_DB:

        d_emb = np.array(chunk["embedding"])

        # cosine similarity (vector alignment)
        similarities = []
        for q_emb in query_embeddings:

            sim = np.dot(q_emb, d_emb) / (
                np.linalg.norm(q_emb) *
                np.linalg.norm(d_emb)
            )
            similarities.append(sim)
        # ------------------------------------------------------------
        # TAKE BEST MATCH ACROSS QUERY VARIANTS
        # ------------------------------------------------------------
        cosine_score = max(similarities)

        
        # ------------------------------------------------------------
        # FILTER LOW-QUALITY MATCHES
        # ------------------------------------------------------------
        # Prevent irrelevant chunks from entering retrieval.
        #
        # WHY IMPORTANT?
        # --------------
        # Without filtering:
        # - unrelated chunks still get reranked
        # - LLM receives noisy context
        # - hallucinations increase
        #
        # Only semantically relevant chunks survive.
        # ------------------------------------------------------------
        if cosine_score < MIN_SIMILARITY_SCORE:
            continue

       
        # ------------------------------------------------------------
        # METADATA BOOSTING
        # ------------------------------------------------------------
        # Metadata can improve retrieval precision.
        #
        # Example:
        # - matching concept names
        # - trusted sources
        # - shorter cleaner chunks
        # ------------------------------------------------------------
        metadata = chunk.get("metadata", {})
        metadata_bonus = 0.0
        concept = metadata.get("concept", "").lower()
        query_lower = query.lower()
        # Boost if query mentions the same concept
        if concept and concept in query_lower:
            metadata_bonus += 0.15

        scored.append(
            RetrievalChunkDTO(
                text=chunk["text"],
                source=metadata["source"] if metadata else "unknown",
                concept=metadata["concept"] if metadata else "unknown",
                length=metadata["length"] if metadata else 0,
                cosine_score=float(cosine_score + metadata_bonus),
            )
       )

    # ------------------------------------------------------------
    # 3. Sort by cosine similarity (recall stage)
    # ------------------------------------------------------------
    scored.sort(key=lambda x: x.cosine_score, reverse=True)

    # ------------------------------------------------------------
    # 4. Expand candidate pool (IMPORTANT FIX)
    # ------------------------------------------------------------
    # We take more than top_k to avoid losing strong matches
    top_candidates = scored[:30]

    # ------------------------------------------------------------
    # NO RELEVANT DOCUMENTS FOUND
    # ------------------------------------------------------------
    # Why this matters
    # Without this:
    # empty retrieval may crash reranker
    # or send empty pairs to model
    # Now your pipeline becomes safe.
    if not top_candidates:
        return RetrievalResponseDTO(
            results=[]
        )

    print(f"[SEARCH] candidates sent to reranker: {len(top_candidates)}")

    # ------------------------------------------------------------
    # 5. Rerank using cross-encoder (precision stage)
    # ------------------------------------------------------------
    reranked: List[RetrievalChunkDTO] = rerank(query, top_candidates)

    for doc in reranked[:top_k]:
        print(
            f"[RAG]"
            f" source={doc.source}"
            f" cosine={doc.cosine_score:.4f}"
            f" rerank={doc.rerank_score:.4f}"
            f" hybrid={doc.hybrid_score:.4f}"
        )
    # ------------------------------------------------------------
    # 7. Final ranking based on hybrid score
    # ------------------------------------------------------------
    reranked.sort(key=lambda x: x.hybrid_score, reverse=True)

    # ------------------------------------------------------------
    # 8. CONFIDENCE FILTERING
    # ------------------------------------------------------------
    # If the best retrieved chunk is too weak,
    # the system should avoid generating an answer.
    #
    # This dramatically reduces hallucinations.
    # ------------------------------------------------------------
  
    best_score = reranked[0].hybrid_score if reranked else 0.0
    print(f"[RAG] best hybrid score: {best_score:.4f}")

    if best_score < MIN_CONFIDENCE_SCORE:

        print("[RAG] retrieval confidence too low")

        return RetrievalResponseDTO(results=[])

    # ------------------------------------------------------------
    # 9. Return top-k results
    # ------------------------------------------------------------
    return RetrievalResponseDTO(
        results=reranked[:top_k]
    )