from app.services.fireworks_service import FireworksClient

fireworks = FireworksClient()


def run_doc_agent(user_message: str, doc_type: str):

    prompt = f"""
You are a startup documentation expert.

Create a professional {doc_type}.

Content:
{user_message}

Make it structured, investor-ready, and clear.
"""

    return fireworks.generate_response(
        user_message=prompt,
        memory_context="",
        model="accounts/fireworks/models/glm-5p2",
        max_tokens=1500,
    )
