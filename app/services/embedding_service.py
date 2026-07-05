import requests
from app.config import settings

def create_embedding(text: str):

    response = requests.post(
        "https://api.fireworks.ai/inference/v1/embeddings",
        headers={
            "Authorization": f"Bearer {settings.FIREWORKS_API_KEY}"
        },
        json={
            "model": settings.EMBEDDING_MODEL,
            "input": text
        }
    )

    response.raise_for_status()

    return response.json()["data"][0]["embedding"]
