from typing import List
from app.v1.modules.rag.dto.retrieval_dto import RetrievalChunkDTO

# ------------------------------------------------------------
# CONFIGURATION
# ------------------------------------------------------------
# Controls batching size for inference safety.
# Large batches can cause:
# - memory spikes
# - GPU/CPU saturation
# ------------------------------------------------------------
BATCH_SIZE = 32

class RerankingService:
    def __init__(self, container):
        self.container = container

    def rerank_candidates(
        self,
        query: str,
        candidates: List[RetrievalChunkDTO]
    ) -> List[RetrievalChunkDTO]:
        """
        CROSS-ENCODER RERANKING ENGINE
        ==============================

        PURPOSE
        -------
        Improve retrieval precision by re-evaluating retrieved chunks
        using a cross-encoder reranking model.

        WHY THIS STEP EXISTS
        --------------------
        Vector search is VERY GOOD for:
        - fast retrieval
        - semantic recall
        - broad matching

        BUT vector similarity is still approximate.

        Example:
        --------
        Query:
            "What is quantum teleportation?"

        Vector search may retrieve:
            - quantum teleportation
            - entanglement
            - cryptography
            - qubits

        because embeddings capture broad semantic relationships.

        The reranker solves this problem by asking:

            "Which chunk BEST answers the query?"

        IMPORTANT:
        ----------
        This is usually the MOST IMPORTANT precision layer
        in a production RAG pipeline.

        INPUT
        -----
        query:
            Original user query.

        docs:
            Candidate chunks retrieved from vector search.

        OUTPUT
        ------
        Same RetrievalChunkDTO objects enriched with:
            - rerank_score
            - hybrid_score

        Then sorted by final relevance.
        """

        # ------------------------------------------------------------
        # STEP 0: SAFETY CHECK
        # ------------------------------------------------------------
        # WHY THIS EXISTS:
        # Prevent unnecessary model inference when no documents exist.
        #
        # Without this:
        # - useless computation occurs
        # - possible batching edge-case bugs
        # - wasted GPU/CPU resources
        # ------------------------------------------------------------
        if not  candidates:
            return []

        # ------------------------------------------------------------
        # STEP 1: BUILD QUERY-DOCUMENT PAIRS
        # ------------------------------------------------------------
        # Cross-encoder rerankers work on PAIRS:
        #
        #   (query, document)
        #
        # The model jointly reads BOTH texts and predicts:
        #
        #   "How relevant is this document to this query?"
        #
        # IMPORTANT:
        # ----------
        # This is VERY different from embeddings.
        #
        # Embeddings:
        #   query -> vector
        #   doc -> vector
        #
        # Cross-encoder:
        #   query + doc together -> relevance score
        #
        # WHY THIS IS POWERFUL:
        # ---------------------
        # The model can deeply understand:
        # - context
        # - wording
        # - semantic intent
        # - educational meaning
        #
        # Example:
        # --------
        # Query:
        #   "What is teleportation?"
        #
        # Chunk:
        #   "Quantum teleportation transfers a quantum state..."
        #
        # The reranker understands this is a DIRECT answer.
        # ------------------------------------------------------------
        pairs = [(query, doc.text) for doc in candidates]

        # ------------------------------------------------------------
        # STEP 2: BATCHED MODEL INFERENCE
        # ------------------------------------------------------------
        # WHY BATCHING EXISTS:
        # --------------------
        # Sending ALL pairs at once may:
        # - overload memory
        # - crash GPU
        # - slow inference dramatically
        #
        # So we process documents in smaller groups.
        #
        # EXAMPLE:
        # --------
        # If BATCH_SIZE = 8:
        #
        # batch 1 -> docs 0..7
        # batch 2 -> docs 8..15
        # etc.
        # ------------------------------------------------------------
        for i in range(0, len(pairs), BATCH_SIZE):

            # --------------------------------------------------------
            # EXTRACT CURRENT BATCH OF QUERY-DOC PAIRS
            # --------------------------------------------------------
            # Example:
            #
            # [
            #   ("what is quantum", "quantum computing ..."),
            #   ("what is quantum", "qubits are ...")
            # ]
            # --------------------------------------------------------
            batch_pairs = pairs[i:i + BATCH_SIZE]

            # --------------------------------------------------------
            # EXTRACT MATCHING DTO OBJECTS
            # --------------------------------------------------------
            # WHY IMPORTANT:
            # --------------
            # We need to attach returned scores back
            # to the correct RetrievalChunkDTO objects.
            #
            # Without this:
            # - scores may attach to wrong chunks
            # - ranking becomes corrupted
            # --------------------------------------------------------
            batch_docs = candidates[i:i + BATCH_SIZE]

            # --------------------------------------------------------
            # STEP 2A: RUN CROSS-ENCODER MODEL
            # --------------------------------------------------------
            # The reranker predicts semantic relevance scores.
            #
            # Example output:
            # [
            #   0.91,
            #   0.42,
            #   0.12
            # ]
            #
            # Higher score = more relevant.
            #
            # IMPORTANT:
            # ----------
            # This is usually MUCH more accurate
            # than cosine similarity alone.
            # --------------------------------------------------------
            batch_scores = self.container.reranker.predict(
                batch_pairs
            )

            # --------------------------------------------------------
            # STEP 2B: ATTACH SCORES TO DOCUMENTS
            # --------------------------------------------------------
            # WHY THIS EXISTS:
            # ----------------
            # Each score must be stored inside its corresponding DTO.
            #
            # zip():
            # ------
            # Combines:
            #
            #   doc1 -> score1
            #   doc2 -> score2
            #
            # safely in order.
            #
            # float(score):
            # -------------
            # Ensures stable Python float type.
            #
            # Some ML libraries return:
            # - numpy.float32
            # - tensors
            #
            # which may later cause serialization issues.
            # --------------------------------------------------------

            for doc, score in zip(batch_docs, batch_scores):
                doc.rerank_score = float(score)

        # ------------------------------------------------------------
        # STEP 3: COMPUTE HYBRID SCORE
        # ------------------------------------------------------------
        # WHY HYBRID SCORING EXISTS:
        # --------------------------
        # Rerankers are VERY accurate,
        # but embeddings still provide useful recall signals.
        #
        # We combine BOTH:
        #
        #   rerank_score -> precision
        #   cosine_score -> semantic recall
        #
        # WHY THIS HELPS:
        # ---------------
        # Prevents reranker overconfidence.
        #
        # Example:
        # --------
        # A chunk may:
        # - have excellent wording
        # - but weak semantic relation
        #
        # Cosine similarity helps stabilize ranking.
        #
        # CURRENT WEIGHTS:
        # ----------------
        # 70% reranker
        # 30% vector similarity
        #
        # WHY?
        # ----
        # Cross-encoders are usually more accurate.
        # ------------------------------------------------------------
        for doc in candidates:

            doc.hybrid_score = (

                # Strong semantic precision signal
                0.7 * (doc.rerank_score or 0.0)

                +

                # Embedding recall stabilization
                0.3 * (doc.cosine_score or 0.0)
            )

        
        # ------------------------------------------------------------
        # STEP 4: FINAL SORTING
        # ------------------------------------------------------------
        # WHY SORTING EXISTS:
        # -------------------
        # Highest quality chunks must appear FIRST.
        #
        # The LLM usually pays more attention
        # to early context chunks.
        #
        # reverse=True:
        # -------------
        # Sort descending:
        #
        # highest score -> first
        #
        # IMPORTANT:
        # ----------
        # We sort using hybrid_score because it is our FINAL
        # combined ranking signal.
        # ------------------------------------------------------------
       
        candidates.sort(
            key=lambda x: x.hybrid_score or 0.0,
            reverse=True
        )

        # ------------------------------------------------------------
        # FINAL OUTPUT
        # ------------------------------------------------------------
        # Returns:
        # - same DTO objects
        # - enriched with rerank_score
        # - enriched with hybrid_score
        # - sorted by final relevance
        #
        # Next pipeline stages may:
        # - diversify
        # - assign reasoning roles
        # - build LLM context
        # ------------------------------------------------------------
        # Remove noise
        MIN_RERANK_SCORE = 0.25
        candidates = [
            doc
            for doc in  candidates
            if (doc.rerank_score or -999) >= MIN_RERANK_SCORE
        ]
        return  candidates