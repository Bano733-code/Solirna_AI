from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    VectorParams,
    PointStruct,
    Filter,
    FieldCondition,
    MatchValue,
)

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
    """
    Creates a fresh collection using the correct vector size.

    NOTE:
    This deletes the old collection.
    Use ONLY while fixing the vector dimension mismatch.
    """

    # Delete old collection if it exists
    if client.collection_exists(COLLECTION):
        print(f"Deleting old collection: {COLLECTION}")
        client.delete_collection(COLLECTION)

    # Create new collection
    print(f"Creating collection: {COLLECTION}")

    client.create_collection(
        collection_name=COLLECTION,
        vectors_config=VectorParams(
            size=4096,      # qwen3-embedding-8b dimension
            distance=Distance.COSINE,
        ),
    )

    # Create payload index
    client.create_payload_index(
        collection_name=COLLECTION,
        field_name="user_id",
        field_schema="integer",
    )

    print("Collection created successfully.")


# -----------------------------
# STORE MEMORY
# -----------------------------
def upload_memory(
    memory_id: str,
    embedding: list,
    payload: dict,
):

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
# SEARCH MEMORY
# -----------------------------
def search_memories(
    user_id: int,
    query_embedding: list,
    limit: int = 5,
):

    results = client.query_points(
        collection_name=COLLECTION,
        query=query_embedding,
        limit=limit,
        query_filter=Filter(
            must=[
                FieldCondition(
                    key="user_id",
                    match=MatchValue(value=user_id),
                )
            ]
        ),
    )

    return results.points
