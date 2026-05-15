import json
from groq import Groq
from app.core.settings import Settings


def get_groq_client(settings: Settings) -> Groq:
    return Groq(api_key=settings.GROAI_API_KEY)

def groq_llm_call(client: Groq, prompt: str) -> str:
    """
    Call Groq LLaMA for natural-language generation.
    No JSON. No strict formatting.
    """

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content
