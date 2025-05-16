from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    
    # Qdrant URL and API Key
    QDRANT_HOST: str | None = "localhost"
    QDRANT_API_KEY: str | None = None
    QDRANT_PORT: int | None = 6333
    
    
    # Qdrant Collection (for both local and cloud)
    QDRANT_COLLECTION_NAME: str = "celebrities"
    QDRANT_VECTOR_DIMENSIONS: int = 512
    
    # Hugging Face Dataset Name
    DATASET_NAME: str = "lansinuote/simple_facenet"


settings = Settings()

print(settings)
