import json
import os
from groq import Groq
from app.core.settings import settings

client = Groq(api_key=settings.GROAI_API_KEY)

print("Groq imported successfully!")
def groq_llm_call(prompt: str, debug: bool = False) -> dict:
    """
    Calls a Groq model and expects pure JSON in the response.
    """
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
             {
                "role": "system",
                "content": (
                    "You are a strict JSON generator. "
                    "You ONLY respond with valid JSON, no explanations, no extra text."
                ),
            },
            {
                "role": "user", 
                "content": prompt,
            }
        ],
        response_format={"type": "json_object"}
    )
    content =  response.choices[0].message.content

    if debug:
        print("Raw LLM response content: 👹👹", content)
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        # Fallback: try to extract JSON or raise
        print("LLM returned invalid JSON:", content)
        raise ValueError(f"Model did not return valid JSON: {content}")