# llm_generator.py
# ----------------
# This module is responsible for the FINAL STEP of the RAG pipeline:
# taking the retrieved text chunks and generating a clean, human-readable
# answer using an LLM (Groq, OpenAI, Claude, etc.).
#
# The retriever finds relevant chunks.
# The reranker orders them by relevance.
# THIS module turns those chunks into a final answer.


from app.ai_core.llms.groq_llm import groq_llm_call
# This is your unified LLM client.
# It hides the details of which provider you're using (Groq/OpenAI/etc.).
# You simply pass a prompt → it returns the model's answer.


def build_prompt(query: str, context_chunks: list[str]) -> str:
    """
    Build the final RAG prompt that will be sent to the LLM.

    WHY THIS FUNCTION EXISTS:
    -------------------------
    - LLMs need a clean, structured prompt.
    - We must clearly separate:
        1. The retrieved context
        2. The user question
        3. The instructions
    - This ensures the LLM answers ONLY using the provided context.
    """

    # Join all retrieved chunks into one block of text.
    # We separate them with "---" so the LLM understands they are distinct pieces.
    context = "\n\n---\n\n".join(context_chunks)

    # This is the standard RAG prompt format used by enterprise systems.
    # It forces the LLM to:
    # - Use ONLY the provided context
    # - Avoid hallucinating
    # - Produce a clean final answer
    prompt = f"""
    You are a helpful assistant. Use ONLY the context below to answer the question.
    If the answer is not in the context, say "I don't know."

    CONTEXT:
    {context}

    QUESTION:
    {query}

    FINAL ANSWER:
    """

    # Strip removes extra whitespace at the start/end.
    return prompt.strip()



def generate_answer(query: str, chunks: list[str]) -> str:
    """
    Generate the final answer using the LLM and the retrieved chunks.

    WHAT THIS FUNCTION DOES:
    ------------------------
    1. Builds the RAG prompt using the retrieved chunks.
    2. Sends the prompt to the LLM.
    3. Returns the LLM's clean, final answer.

    WHY THIS IS IMPORTANT:
    ----------------------
    - The retriever gives you raw text (sometimes messy).
    - The LLM rewrites it into a clean explanation.
    - This is the step that transforms your system from "vector search"
      into a real AI assistant.
    """

    # 1. Build the final prompt
    prompt = build_prompt(query, chunks)

    # 2. Call your LLM provider (Groq, OpenAI, Claude, etc.)
    #    The llm_client abstracts away the provider details.
    response = groq_llm_call(prompt)

    # 3. Return the final answer
    return response
