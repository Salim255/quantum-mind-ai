# This dictionary defines the schema for the "embed_text" tool.
# It is consumed by your agent_core so the LLM knows:
# - the tool name
# - what the tool does
# - what parameters it expects
# - how to structure the JSON when calling it

embed_tool_schema = {
    "type": "function",  
    # "type" tells the LLM that this is a callable tool.
    # Other types could be "object" or "array", but "function" means:
    # "You can call this tool with arguments."

    "function": {
        "name": "embed_text",
        # The name the LLM will use when generating a tool call.
        # Example of a tool call the LLM might produce:
        # { "tool": "embed_text", "text": "What is a qubit?" }

        "description": (
            "Generate a semantic embedding vector for quantum learning content. "
            "Used for retrieving relevant explanations, lessons, formulas, and examples "
            "inside the QuantumMind AI learning system."
        ),
        # This description helps the LLM understand WHEN to call this tool.
        # The more specific the description, the smarter the tool usage.

        "parameters": {
            "type": "object",
            # The tool expects a JSON object as input.
            # Example:
            # { "text": "...", "source": "lesson" }

            "properties": {
                "text": {
                    "type": "string",
                    "description": (
                        "The text to embed. This may be a user question, a lesson chunk, "
                        "a quantum explanation, a formula description, or any learning content."
                    )
                },
                # "text" is the core input: the raw content that will be converted
                # into a high‑dimensional embedding vector.

                "source": {
                    "type": "string",
                    "enum": ["user_query", "lesson", "document", "example", "formula"],
                    "description": (
                        "Indicates the origin of the text. Helps the AI adapt retrieval "
                        "and reasoning for quantum learning."
                    )
                },
                # "source" is optional but extremely useful.
                # It lets your AI know what kind of content is being embedded.
                # This allows smarter ranking and retrieval.

                "normalize": {
                    "type": "boolean",
                    "description": (
                        "Whether to L2-normalize the embedding vector. "
                        "Defaults to True for consistent retrieval."
                    ),
                    "default": True
                }
                # "normalize" ensures all vectors have the same magnitude.
                # This improves cosine similarity and retrieval accuracy.
            },

            "required": ["text"]
            # Only "text" is required.
            # "source" and "normalize" are optional.
            # This keeps the tool flexible while still enforcing correctness.
        }
    }
}
