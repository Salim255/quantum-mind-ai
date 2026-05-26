from groq import Groq

# ------------------------------------------------------------------
# LLM CALL
# ------------------------------------------------------------------

def groq_llm_call_streaming(
    client: Groq,
    prompt: str
    ):
    """
    Call the Groq-hosted LLM for grounded RAG generation.

    PURPOSE
    -------
    This function sends:
    - the system instructions
    - the user prompt
    - retrieved context

    to the language model.

    IMPORTANT
    ---------
    In RAG systems, prompt engineering is critical.

    A weak system prompt causes:
    - hallucinations
    - vague summaries
    - generic answers
    - ignored context

    A strong system prompt improves:
    - grounding
    - relevance
    - factual accuracy
    - concise explanations
    """

    # --------------------------------------------------------------
    # SYSTEM PROMPT
    # --------------------------------------------------------------
    #
    # The system prompt defines:
    # - assistant behavior
    # - answer style
    # - grounding rules
    # - hallucination prevention
    #
    # This is one of the MOST important parts
    # of a production RAG system.
    #
    system_prompt = """
    You are a highly accurate educational AI assistant.

    Your job is to answer the user's question ONLY using the provided context.

    RULES:
    - Use the retrieved context as the primary source of truth.
    - Do NOT invent information not present in the context.
    - If the answer is unclear from the context, say so honestly.
    - Be concise, clear, and educational.
    - Explain concepts simply when possible.
    - Do NOT summarize the entire document.
    - Focus specifically on answering the user's question.
    - Prefer direct explanations over long introductions.
    """

    # --------------------------------------------------------------
    # SEND REQUEST TO GROQ
    # --------------------------------------------------------------
    #
    # We use:
    # - system role → controls assistant behavior
    # - user role → contains the RAG prompt/context
    #
    stream = client.chat.completions.create(

        # ----------------------------------------------------------
        # MODEL
        # ----------------------------------------------------------
        #
        # llama-3.1-8b-instant:
        # - fast
        # - low latency
        # - good for educational RAG
        #
        model="llama-3.1-8b-instant",

        # ----------------------------------------------------------
        # CONVERSATION MESSAGES
        # ----------------------------------------------------------
        messages=[

            # System behavior instructions.
            {
                "role": "system",
                "content": system_prompt
            },

            # Final RAG prompt containing:
            # - user question
            # - retrieved context
            {
                "role": "user",
                "content": prompt
            }
        ],
        response_format={"type": "json_object"},
        max_tokens=300,
        timeout=10,
        stream=True
    )
    

    # --------------------------------------------------------------
    # EXTRACT FINAL MODEL RESPONSE
    # --------------------------------------------------------------
    #
    # Groq returns:
    #
    # response.choices[0].message.content
    #
    # which contains the generated answer text.
    #
   

    for chunk in stream:
        data = chunk.choices[0].delta.content
        yield data

   


def groq_llm_call(
    client: Groq,
    prompt: str
) -> str:
    """
    Call the Groq-hosted LLM for grounded RAG generation.

    PURPOSE
    -------
    This function sends:
    - the system instructions
    - the user prompt
    - retrieved context

    to the language model.

    IMPORTANT
    ---------
    In RAG systems, prompt engineering is critical.

    A weak system prompt causes:
    - hallucinations
    - vague summaries
    - generic answers
    - ignored context

    A strong system prompt improves:
    - grounding
    - relevance
    - factual accuracy
    - concise explanations
    """

    # --------------------------------------------------------------
    # SYSTEM PROMPT
    # --------------------------------------------------------------
    #
    # The system prompt defines:
    # - assistant behavior
    # - answer style
    # - grounding rules
    # - hallucination prevention
    #
    # This is one of the MOST important parts
    # of a production RAG system.
    #
    system_prompt = """
    You are a highly accurate educational AI assistant.

    Your job is to answer the user's question ONLY using the provided context.

    RULES:
    - Use the retrieved context as the primary source of truth.
    - Do NOT invent information not present in the context.
    - If the answer is unclear from the context, say so honestly.
    - Be concise, clear, and educational.
    - Explain concepts simply when possible.
    - Do NOT summarize the entire document.
    - Focus specifically on answering the user's question.
    - Prefer direct explanations over long introductions.
    """

    # --------------------------------------------------------------
    # SEND REQUEST TO GROQ
    # --------------------------------------------------------------
    #
    # We use:
    # - system role → controls assistant behavior
    # - user role → contains the RAG prompt/context
    #
    stream = client.chat.completions.create(

        # ----------------------------------------------------------
        # MODEL
        # ----------------------------------------------------------
        #
        # llama-3.1-8b-instant:
        # - fast
        # - low latency
        # - good for educational RAG
        #
        model="llama-3.1-8b-instant",

        # ----------------------------------------------------------
        # CONVERSATION MESSAGES
        # ----------------------------------------------------------
        messages=[

            # System behavior instructions.
            {
                "role": "system",
                "content": system_prompt
            },

            # Final RAG prompt containing:
            # - user question
            # - retrieved context
            {
                "role": "user",
                "content": prompt
            }
        ],
        response_format={"type": "json_object"},
        max_tokens=300,
        timeout=10,
    )
    

    # --------------------------------------------------------------
    # EXTRACT FINAL MODEL RESPONSE
    # --------------------------------------------------------------
    #
    # Groq returns:
    #
    # response.choices[0].message.content
    #
    # which contains the generated answer text.
    #
    full_response = ""

    for chunk in stream:
        if chunk.choices[0].delta.content:
            full_response += chunk.choices[0].delta.content

    return full_response
