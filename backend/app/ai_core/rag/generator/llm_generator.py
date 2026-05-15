# llm_generator.py
# ----------------
# This module is responsible for the FINAL STEP of the RAG pipeline:
# taking the retrieved text chunks and generating a clean, human-readable
# answer using an LLM (Groq, OpenAI, Claude, etc.).
#
# The retriever finds relevant chunks.
# The reranker orders them by relevance.
# THIS module turns those chunks into a final answer.

from groq import Groq
from app.ai_core.llms.groq_llm import groq_llm_call
from app.ai_core.rag.prompt.rag_prompt_builder import RAGPromptBuilder
# This is your unified LLM client.
# It hides the details of which provider you're using (Groq/OpenAI/etc.).
# You simply pass a prompt → it returns the model's answer.


def generate_answer(query: str, chunks: list[str], client: Groq) -> str:
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
    prompt = RAGPromptBuilder.build(query, chunks)

    # 2. Call your LLM provider (Groq, OpenAI, Claude, etc.)
    #    The llm_client abstracts away the provider details.
    response = groq_llm_call(client, prompt)

    # 3. Return the final answer
    return response
