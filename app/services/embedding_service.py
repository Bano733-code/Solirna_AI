import requests
from app.config import settings

EMBEDDING_URL = "https://api.fireworks.ai/inference/v1/embeddings"


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
    
    print("Status:", response.status_code)
    print("Response:", response.text)



    response.raise_for_status()

    return response.json()["data"][0]["embedding"]
    print("VECTOR SIZE:", len(embedding))
    return embedding
