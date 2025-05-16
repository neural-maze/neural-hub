import os

from zenml.client import Client
from dotenv import load_dotenv

load_dotenv()

client = Client()

client.create_secret(
    name="qdrant",
    values={"QDRANT_URL": os.getenv("QDRANT_URL"), "QDRANT_PORT": os.getenv("QDRANT_PORT")}
)
