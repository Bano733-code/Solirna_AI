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

    collections = client.get_collections().collections
    names = [c.name for c in collections]


    if COLLECTION not in names:

        client.create_collection(
            collection_name=COLLECTION,
            vectors_config=VectorParams(
                # CHANGE THIS TO YOUR EMBEDDING SIZE
                # qwen3-embedding-8b dimension
                size=4096,
                distance=Distance.COSINE,
            ),
        )


    # Create payload index for user_id filtering
    # Required for query_points filter
    client.create_payload_index(
        collection_name=COLLECTION,
        field_name="user_id",
        field_schema="integer",
    )



# -----------------------------
# STORE MEMORY
# -----------------------------
def upload_memory(
    memory_id: str,
    embedding: list,
    payload: dict
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
                    match=MatchValue(
                        value=user_id
                    ),
                )
            ]
        ),
    )

    return results.points
