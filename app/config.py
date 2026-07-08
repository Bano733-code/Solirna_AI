from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "Solirna AI"

    API_V1_STR: str = "/api/v1"

    SECRET_KEY: str

    ALGORITHM: str = "HS256"

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24

    DATABASE_URL: str

    FIREWORKS_API_KEY: str

    EMBEDDING_MODEL: str = "BAAI/bge-large-en-v1.5"

    LLM_MODEL: str = "accounts/fireworks/models/glm-5p2"

    # ✅ ADD THESE (Qdrant)
    QDRANT_URL: str
    QDRANT_API_KEY: str
    QDRANT_COLLECTION: str = "solirna_memory"

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
    )


settings = Settings()
