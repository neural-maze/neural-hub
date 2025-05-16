
from datasets import (Dataset, load_dataset,  # type: ignore
                      load_dataset_builder)
from zenml import step
from zenml.logger import get_logger

from settings import settings

logger = get_logger(__name__)

@step
def load_hf_dataset(dataset_name: str = "lansinuote/simple_facenet") -> Dataset:
    """Loads and returns the HuggingFace dataset for facial recognition.
    
    This function loads the dataset specified by DATASET_NAME constant using the
    HuggingFace datasets library. It prints information about available splits
    and the size of the training dataset.
    
    Args:
        dataset_name: The name of the dataset to load.
        
    Returns:
        dict: A dictionary containing the loaded dataset with 'train' as the key
            and the corresponding dataset object as the value.
    """
    dataset_builder = load_dataset_builder(settings.DATASET_NAME)
    logger.info(f"Available splits:\n{dataset_builder.info.splits}")
    
    dataset = load_dataset(dataset_name, split="train")
    logger.info(f"Number of samples in the dataset: {len(dataset)}")
    
    return dataset


@step
def sample_dataset(dataset: Dataset, sample_size: int = 3000) -> Dataset:
    """Creates a random sample of the given dataset.

    Args:
        dataset (Dataset): The input dataset to sample from.
        sample_size (int, optional): Number of samples to select. Defaults to 3000.

    Returns:
        Dataset: A new dataset containing the random sample.
    """
    sampled_dataset = dataset.shuffle(seed=42).select(range(sample_size))
    logger.info(f"Number of samples in the sampled dataset: {len(sampled_dataset)}")

    return sampled_dataset
