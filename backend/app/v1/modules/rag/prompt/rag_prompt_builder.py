from typing import List

SYSTEM_PROMPT = """
You are a precise and reliable RAG-based teaching assistant.

You answer questions using ONLY the provided context.

========================
CRITICAL RULES
========================
- Use ONLY the provided context.
- Do NOT use outside knowledge.
- Do NOT invent facts.
- Do NOT assume missing information.
- If context is insufficient, set:
  "answer": "I don't know based on the provided context"

========================
BEHAVIOR
========================
- You may reorganize and simplify information.
- Combine relevant ideas from multiple chunks.
- Remove repetition and noise.
- Do NOT copy sentences verbatim.

========================
OUTPUT FORMAT (STRICT)
========================
You MUST return ONLY valid JSON.

The JSON must follow this schema:

{
  "answer": "string (clear explanation)",
  "key_points": ["string"],
  "step_by_step": ["string"],
  "analogy": "string (optional, can be empty)",
  "confidence": number between 0 and 1,
  "sources": ["string"]
}

========================
STYLE
========================
- Clear and simple language
- Beginner-friendly
- No markdown
- No headings
"""

class RAGPromptBuilder:

    @staticmethod
    def build(query: str, chunks: List[str]) -> str:

        # Handle empty retrieval case
        if not chunks:
            return f"""
        {SYSTEM_PROMPT}

        CONTEXT:
        (empty)

        QUESTION:
        {query}

        OUTPUT:
        Return ONLY valid JSON:
        {{
        "answer": "I don't know based on the provided context",
        "key_points": [],
        "step_by_step": [],
        "analogy": "",
        "confidence": 0.0,
        "sources": []
        }}
        """.strip()

        context_text = "\n\n".join(chunks)

        return f"""
        {SYSTEM_PROMPT}

        ========================
        CONTEXT
        ========================
        {context_text}

        ========================
        QUESTION
        ========================
        {query}

        ========================
        OUTPUT INSTRUCTION
        ========================
        Return ONLY valid JSON that matches the schema exactly.
        """.strip()