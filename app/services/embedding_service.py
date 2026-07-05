from sentence_transformers import SentenceTransformer

# Load the embedding model only once
model = SentenceTransformer("BAAI/bge-large-en-v1.5")


def create_embedding(text: str) -> list[float]:
    """
    Generate a 384-dimensional embedding for the given text.
    """
    embedding = model.encode(text)

    return embedding.tolist()
