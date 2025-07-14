import os
import torch
from PIL import Image
from qdrant_client import QdrantClient
from rich.console import Console
from rich.markdown import Markdown
import ollama
from src.vision_model_loader import get_colqwen_model, get_colqwen_processor, device

console = Console()

def vision_rag(user_query: str):
    
    colqwen_model = get_colqwen_model()
    colqwen_processor = get_colqwen_processor()

    QDRANT_URL = os.getenv("QDRANT_URL")
    QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
    QDRANT_COLLECTION_NAME = os.getenv("QDRANT_COLLECTION_NAME")
    DATA_FOLDER_PATH = os.getenv("DATA_FOLDER_PATH")
    PNG_FOLDER_PATH = os.path.join(DATA_FOLDER_PATH, "png")

    qdrant_client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)

    text_input = colqwen_processor(text=user_query)
    text_input = {k: v.to(device) for k, v in text_input.items()}

    with torch.no_grad():
        text_embeddings = colqwen_model(**text_input).embeddings
    text_embeddings = text_embeddings.squeeze(0).cpu().tolist()

    results = qdrant_client.query_points(
        collection_name=QDRANT_COLLECTION_NAME,
        query=text_embeddings,
        with_payload=True,
        limit=1,
    )

    retrieved_points = results.points[0]
    pdf_filename = retrieved_points.payload["pdf_name"]
    page = str(retrieved_points.payload["page"])
    png_filename = os.path.splitext(pdf_filename)[0] + "-" + page + "_1" +  ".png"
    filename_path = os.path.join(PNG_FOLDER_PATH, png_filename)

    image = Image.open(filename_path).convert("RGB")
    image.show()

    response = ollama.chat(
        model='gemma3:27b',
        messages=[
            {
                'role': 'system',
                'content': (
                    "You're an expert AI assistant specialized on analyzing medical images and answering user queries."
                )
            },
            {
                'role': 'user',
                'content': user_query,
                'images': [filename_path]
            }
        ]
    )

    md = Markdown(response['message']['content'])
    console.print(md)