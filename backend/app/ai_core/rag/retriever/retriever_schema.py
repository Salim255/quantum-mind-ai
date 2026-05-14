# ---------------------------------------------------------------------------
# This schema defines the "search_documents" tool.
# It tells the LLM:
# - the tool name
# - what the tool does
# - what parameters it expects
# - how to structure the JSON when calling it
#
# This tool is used during retrieval‑augmented generation (RAG).
# When the LLM needs context from your quantum knowledge base,
# it will automatically call this tool to fetch relevant text chunks.
# ---------------------------------------------------------------------------

retriever_tool_schema = {
    "type": "function",
    # "type" tells the LLM that this is a callable tool.
    # The model can generate a tool call like:
    # { "tool": "search_documents", "query": "What is a qubit?" }

    "function": {
        "name": "search_documents",
        # The name exposed to the LLM.
        # Must match the name your agent_core expects.

        "description": (
            "Retrieve the most relevant documents for a query. "
            "Used by the QuantumMind AI system to fetch lesson chunks, "
            "explanations, formulas, and examples related to the user's question."
        ),
        # This description helps the LLM understand WHEN to call this tool.
        # The more specific the description, the smarter the tool usage.

        "parameters": {
            "type": "object",
            # The tool expects a JSON object as input.

            "properties": {
                "query": {
                    "type": "string",
                    "description": (
                        "The user query to search for. This will be embedded "
                        "and compared against stored quantum learning content."
                    )
                },
                # "query" is the core input.
                # The LLM will pass the user's question here.

                "top_k": {
                    "type": "integer",
                    "description": (
                        "Optional: number of top results to return. "
                        "Defaults to 3 if not provided."
                    )
                }
                # "top_k" allows the LLM to control how many chunks it wants.
                # Useful for long or complex questions.
            },

            "required": ["query"]
            # Only "query" is mandatory.
            # "top_k" is optional to keep the tool flexible.
        }
    }
}
