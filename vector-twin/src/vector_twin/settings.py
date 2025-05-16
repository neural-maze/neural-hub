from pydantic_settings import BaseSettings, SettingsConfigDict

try:
    from zenml.client import Client
    from zenml.exceptions import EntityExistsError
    
    ZENML_ENVIRONMENT = True

except ImportError:
    ZENML_ENVIRONMENT = False


class Settings(BaseSettings):    
    model_config = SettingsConfigDict(env_file=".env", extra="ignore", env_file_encoding="utf-8")
    
    # Qdrant URL, port and API key
    QDRANT_HOST: str = "localhost"
    QDRANT_URL: str  = ""
    QDRANT_PORT: int = 6333
    QDRANT_API_KEY: str | None = None
    
    # Qdrant Collection (for both local and cloud)
    QDRANT_COLLECTION_NAME: str = "celebrities"
    QDRANT_VECTOR_DIMENSIONS: int = 512
    
    # Hugging Face Dataset Name
    DATASET_NAME: str = "lansinuote/simple_facenet"
    
    @classmethod
    def load_settings(cls):
        """Load settings from ZenML secret store if available."""
        try:
            client = Client()
            secrets = client.get_secret("qdrant")
            if "QDRANT_URL" in secrets.secret_values:
                cls.QDRANT_URL = secrets.secret_values["QDRANT_URL"]
            if "QDRANT_PORT" in secrets.secret_values:
                cls.QDRANT_PORT = int(secrets.secret_values["QDRANT_PORT"])
        except EntityExistsError:
            # Secret not found, use default values
            pass
        return cls()


if ZENML_ENVIRONMENT:
    settings = Settings.load_settings()
else:
    settings = Settings()
