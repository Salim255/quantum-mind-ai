from typing import List

SYSTEM_PROMPT = """
You are a precise and reliable RAG-based teaching assistant.

You answer questions using ONLY the provided context.

RULES:
- Use ONLY the provided context.
- Do NOT use outside knowledge.
- Do NOT invent facts.
- If the context is insufficient, say: "I don't know based on the provided context."

BEHAVIOR:
- You are allowed to reorganize and simplify the information.
- You should combine relevant ideas from multiple chunks.
- You should remove repetition and noise.
- You should NOT copy sentences verbatim.

STYLE:
- Clear and simple explanation
- Beginner-friendly
- Structured for readability
"""

class RAGPromptBuilder:

    @staticmethod
    def build(query: str, chunks: List[str]) -> str:

        if not chunks:
            return f"""
            No relevant context was found.

            Question:
            {query}

            Answer:
            I don't know based on the provided context.
            """.strip()

        context_text = "\n\n".join(chunks)

        prompt = f"""
        {SYSTEM_PROMPT}

        CONTEXT:
        {context_text}

        QUESTION:
        {query}

        TASK:
        Answer the question clearly using ONLY the context.
        Focus on clarity and correctness.
        """.strip()

        return prompt