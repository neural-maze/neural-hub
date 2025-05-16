import click
from pipeline import embedding_pipeline  # type: ignore


@click.command(
    help="""
ZenML Starter project.

Run the ZenML starter project with basic options.

Examples:

  # Run the training pipeline
    python run.py
"""
)
@click.option(
    "--enable-cache",
    is_flag=True,
    default=False,
    help="Enabling caching for the pipeline run.",
)
@click.option(
    "--use-qdrant-cloud",
    is_flag=True,
    default=False,
    help="Whether to use Qdrant Cloud or local Qdrant",
)
def main(
    use_qdrant_cloud: bool,
    enable_cache: bool = False,
):  
    pipeline_args: dict = {}
    
    if not enable_cache:
        pipeline_args["enable_cache"] = False
    
    if use_qdrant_cloud:
        pipeline_args["config_path"] = "src/embedding_pipeline/configs/embedding_generation_qdrant_cloud.yaml"
    else:
        pipeline_args["config_path"] = "src/embedding_pipeline/configs/embedding_generation_local.yaml"

    
    embedding_pipeline.with_options(**pipeline_args)(use_qdrant_cloud=use_qdrant_cloud)


if __name__ == "__main__":
    main()
