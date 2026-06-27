from groq import Groq
from app.config import settings

client = Groq(
    api_key=settings.GROQ_API_KEY
)


def generate_response(
    user_message: str,
    memory_context: str = ""
) -> str:
    """
    Generate a response using the Groq API.
    """

    system_prompt = f"""
You are Solirna AI.

You are an intelligent AI career mentor.

Use previous conversation if it is relevant.

Previous Conversation:
{memory_context}

Always answer naturally, clearly and helpfully.
"""

    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": user_message
            }
        ],
        temperature=0.7,
        max_tokens=1024,
    )

    return completion.choices[0].message.content