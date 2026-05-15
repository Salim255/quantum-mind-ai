# rag/prompt/rag_prompt_builder.py
# ----------------------------------------------------
# Single responsibility:
# Build the FINAL RAG prompt for the LLM generator.
#
# This builder is used AFTER:
#   - retrieval
#   - reranking
#   - selecting top chunks
#
# It does NOT:
#   - call the LLM
#   - validate output
#   - retry
#
# Its ONLY job is to assemble a clean, safe, deterministic
# prompt that the LLM can use to generate the final answer.
# ----------------------------------------------------


class RAGPromptBuilder:
    """
    Build the final RAG prompt used by the LLM generator.

    WHY THIS CLASS EXISTS:
    ----------------------
    - Keeps prompt logic isolated and reusable.
    - Makes your RAG pipeline modular and clean.
    - Allows you to update the prompt in ONE place.
    - Ensures consistent behavior across your entire system.
    """

    @staticmethod
    def build(query: str, context_chunks: list[str]) -> str:
        """
        Build a clean, deterministic RAG prompt.

        PARAMETERS:
        -----------
        query : str
            The user's question.

        context_chunks : list[str]
            The top N retrieved + reranked chunks.
            These are the ONLY facts the LLM is allowed to use.

        RETURNS:
        --------
        str
            A fully assembled prompt ready to be sent to the LLM.
        """

        # ------------------------------------------------------------
        # 1. Merge all retrieved chunks into a single context block.
        #
        # We separate chunks with a clear divider ("---") so the LLM
        # understands they are distinct pieces of information.
        #
        # This improves reasoning and reduces hallucination.
        # ------------------------------------------------------------
        context_text = "\n\n---\n\n".join(context_chunks)

        # ------------------------------------------------------------
        # 2. Build the final prompt.
        #
        # This is the standard enterprise RAG prompt format:
        #   - Clear instruction
        #   - Context block
        #   - User question
        #   - Final answer section
        #
        # The LLM is explicitly told:
        #   - Use ONLY the context
        #   - Say "I don't know" if missing info
        #
        # This prevents hallucinations and ensures reliability.
        # ------------------------------------------------------------
        prompt = f"""
        You are a teacher explaining quantum computing.
        Rewrite the following answer to the question in a clearer,
        more structured way. Keep it correct, but improve clarity.
        and if the answer is not in the context, and say "I don't know."

        CONTEXT:
        {context_text}

        QUESTION:
        {query}

        FINAL ANSWER:
        """

        # Remove leading/trailing whitespace for cleanliness.
        return prompt.strip()
