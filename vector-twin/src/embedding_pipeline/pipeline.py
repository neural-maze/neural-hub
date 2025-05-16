from settings import settings  # type: ignore
from steps import (generate_embeddings, load_hf_dataset,  # type: ignore
                   sample_dataset)
from zenml import pipeline
from zenml.config import DockerSettings
from zenml.config.docker_settings import DockerBuildConfig


docker_settings = DockerSettings(build_config=DockerBuildConfig(dockerignore=".dockerignore"))

@pipeline(settings={"docker": docker_settings})
def embedding_pipeline(use_qdrant_cloud: bool):
    dataset = load_hf_dataset()
    sampled_dataset = sample_dataset(dataset)
    generate_embeddings(sampled_dataset, use_qdrant_cloud)
