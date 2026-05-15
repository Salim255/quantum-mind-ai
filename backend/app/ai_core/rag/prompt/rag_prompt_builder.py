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

SYSTEM_PROMPT = """
You are a STRICT retrieval‑augmented generation (RAG) assistant.

HARD RULES (you MUST follow all of them):
1. You MUST answer ONLY using information explicitly present in the provided context.
2. You MUST NOT add external knowledge, background knowledge, or general domain knowledge.
3. You MUST NOT infer, guess, or assume anything that is not explicitly stated in the context.
4. You MUST NOT add structure such as:
   - headings
   - bullet points
   - numbered lists
   - markdown
   - sections
5. You MUST NOT add examples, analogies, metaphors, or teaching tone.
6. You MUST NOT introduce new concepts unless they appear in the context.
7. You MUST NOT expand, generalize, or elaborate beyond the context.
8. You MUST write in plain text only.
9. If the context does NOT contain enough information to answer the question, you MUST reply exactly:
   "I don't know based on the provided context."

Your output MUST be:
- short
- literal
- factual
- grounded ONLY in the context
- plain text

"""


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
        {SYSTEM_PROMPT}

        CONTEXT:
        {context_text}

        QUESTION:
        {query}

        FINAL ANSWER:
        """

        # Remove leading/trailing whitespace for cleanliness.
        return prompt.strip()
