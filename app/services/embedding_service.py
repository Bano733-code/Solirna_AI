import requests
from app.config import settings

EMBEDDING_URL = "https://api.fireworks.ai/inference/v1/rerank"


def create_embedding(text: str):

    response = requests.post(
        EMBEDDING_URL,
        headers={
            "Authorization": f"Bearer {settings.FIREWORKS_API_KEY}"
        },
        json={
            "model": settings.EMBEDDING_MODEL,
            "input": text
        },
        timeout=30,
    )

    response.raise_for_status()

    return response.json()["data"][0]["embedding"]
