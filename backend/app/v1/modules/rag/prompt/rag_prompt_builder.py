from typing import List

SYSTEM_PROMPT = """
  You are a beginner-friendly quantum computing tutor.

  Rules:
  - Use ONLY the provided context.
  - Do not use outside knowledge.
  - If context is insufficient, say:
    "Sorry! your question must be related to quantum computing."

  Return ONLY valid JSON:

  {
    "answer": "string",
    "analogy": "string"
    "confidence": number,
  }
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
                "analogy": "",
                "confidence": 0.0,
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