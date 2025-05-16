from uuid import uuid4

from datasets import Dataset  # type: ignore
from tqdm import tqdm  # type: ignore
from zenml import step
from zenml.logger import get_logger

from vector_twin.models import initialize_models, process_single_image
from vector_twin.qdrant import get_qdrant_client, create_collection, insert_image_embedding


logger = get_logger(__name__)


@step
def generate_embeddings(dataset: Dataset, use_qdrant_cloud: bool = True) -> None:
    """Generates embeddings for the dataset and stores them in Qdrant vector database.
    
    Args:
        dataset: Dataset containing celebrity images and labels
        use_qdrant_cloud: If True, connects to Qdrant Cloud using URL and API key.
                          If False, connects to local Qdrant instance.
    """
    qdrant_client = get_qdrant_client(use_qdrant_cloud)
    create_collection(qdrant_client)
    
    device, mtcnn, resnet = initialize_models()
    
    for row in tqdm(dataset):
        img_embedding = process_single_image(row["image"], device, mtcnn, resnet)
        insert_image_embedding(qdrant_client, img_embedding, str(uuid4()), row['label'])
