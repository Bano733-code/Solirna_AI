from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct

from app.config import settings

client = QdrantClient(
    url=settings.QDRANT_URL,
    api_key=settings.QDRANT_API_KEY,
)

COLLECTION = settings.QDRANT_COLLECTION


def create_collection():
    """
    Creates the collection if it doesn't already exist.
    """
    collections = client.get_collections().collections
    names = [c.name for c in collections]

    if COLLECTION not in names:
        client.create_collection(
            collection_name=COLLECTION,
            vectors_config=VectorParams(
                size=384,
                distance=Distance.COSINE,
            ),
        )


def upload_memory(memory_id, embedding, payload):
    """
    Store an embedding with its metadata.
    """
    client.upsert(
        collection_name=COLLECTION,
        points=[
            PointStruct(
                id=memory_id,
                vector=embedding,
                payload=payload,
            )
        ],
    )


def search_memories(query_embedding, limit=5):
    """
    Retrieve the most similar memories.
    """
    results = client.search(
        collection_name=COLLECTION,
        query_vector=query_embedding,
        limit=limit,
    )

    return results
