from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct, Filter, FieldCondition, MatchValue

from app.config import settings

client = QdrantClient(
    url=settings.QDRANT_URL,
    api_key=settings.QDRANT_API_KEY,
)

COLLECTION = settings.QDRANT_COLLECTION


# -----------------------------
# CREATE COLLECTION
# -----------------------------
def create_collection():
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


# -----------------------------
# STORE MEMORY
# -----------------------------
def upload_memory(memory_id: str, embedding: list, payload: dict):
    """
    Store memory in Qdrant with metadata.
    Payload MUST include:
    - user_id
    - text
    - type (chat/prd/pitch)
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


# -----------------------------
# SEARCH MEMORY (FIXED)
# -----------------------------
def search_memories(user_id: int, query_embedding: list, limit: int = 5):
    """
    Retrieve ONLY user-specific memories (IMPORTANT FIX)
    """

    results = client.search(
        collection_name=COLLECTION,
        query_vector=query_embedding,
        limit=limit,
        query_filter=Filter(
            must=[
                FieldCondition(
                    key="user_id",
                    match=MatchValue(value=user_id)
                )
            ]
        ),
    )

    return results
