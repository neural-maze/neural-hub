from functools import lru_cache

from qdrant_client import QdrantClient  # type: ignore
from vector_twin.settings import settings  # type: ignore


@lru_cache(maxsize=1)
def get_qdrant_client(use_qdrant_cloud: bool = True) -> QdrantClient:
    """Gets a configured Qdrant client instance.

    Args:
        use_qdrant_cloud (bool, optional): Whether to connect to Qdrant Cloud or local instance. 
            Defaults to True.

    Returns:
        QdrantClient: Configured Qdrant client connected to either cloud or local instance.
    """
    if use_qdrant_cloud:
        return QdrantClient(
            url=settings.QDRANT_URL,
            port=settings.QDRANT_PORT,
            api_key=settings.QDRANT_API_KEY
        )
    else:
        return QdrantClient(
            host=settings.QDRANT_HOST, 
            port=settings.QDRANT_PORT
        )
