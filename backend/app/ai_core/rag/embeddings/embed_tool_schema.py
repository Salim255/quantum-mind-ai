# This dictionary defines the schema for the "embed_text" tool.
# It tells the LLM:
# - the tool name
# - what the tool does
# - what parameters it expects
# - how the parameters must be structured
#
# This schema is consumed by your agent_core, allowing the model
# to automatically call the embedding tool when needed.

embed_tool_schema = {
    "type": "function",  # Indicates this is a callable tool
    "function": {
        "name": "embed_text",  # The name the LLM will use to call the tool
        "description": "Generate an embedding vector for a given text.",  # Human-readable description
        "parameters": {
            "type": "object",  # The tool expects a JSON object
            "properties": {
                "text": {"type": "string"}  # The only required field: the text to embed
            },
            "required": ["text"]  # The LLM MUST provide "text"
        }
    }
}