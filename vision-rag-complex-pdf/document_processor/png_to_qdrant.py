import os
import re
import json
from pathlib import Path
from dotenv import load_dotenv
import torch
from PIL import Image
from qdrant_client import QdrantClient, models
from qdrant_client.models import PointStruct
from src.vision_model_loader import get_colqwen_model, get_colqwen_processor, device

load_dotenv(".env")

colqwen_model = get_colqwen_model()
colqwen_processor = get_colqwen_processor()

DATA_FOLDER_PATH = os.getenv("DATA_FOLDER_PATH")
PNG_FOLDER_PATH = os.path.join(DATA_FOLDER_PATH, "png")
METADATA_PATH = os.path.join(DATA_FOLDER_PATH, "metadata.json")

with open(METADATA_PATH, "r") as f:
    metadata_list = json.load(f)

metadata_map = {
    os.path.splitext(entry["pdf_name"])[0]: entry for entry in metadata_list
}

qdrant_url = os.getenv("QDRANT_URL")
qdrant_api_key = os.getenv("QDRANT_API_KEY")
collection_name = os.getenv("QDRANT_COLLECTION_NAME")
batch_size = 5

client = QdrantClient(url=qdrant_url, api_key=qdrant_api_key)

client.recreate_collection(
    collection_name=collection_name,
    vectors_config=models.VectorParams(
        size=128,
        distance=models.Distance.COSINE,
        multivector_config=models.MultiVectorConfig(
            comparator=models.MultiVectorComparator.MAX_SIM
        ),
    ),
)

points = []

image_paths = list(Path(PNG_FOLDER_PATH).glob("*.png"))

for idx, path in enumerate(image_paths):

    match = re.match(r"(.+)-(\d+)_\d+\.png", path.name)

    if not match:

        print(f"⚠️  Nombre de archivo no válido: {path.name}")
        continue

    base_name = match.group(1)
    page = int(match.group(2))

    metadata = metadata_map.get(base_name)

    if not metadata:

        print(f"⚠️  No se encontraron metadatos para: {base_name}")
        continue

    try:

        image = Image.open(path).convert("RGB")
        inputs = colqwen_processor(images=image)
        inputs = {k: v.to(device) for k, v in inputs.items()}

        with torch.no_grad():

            embedding = colqwen_model(**inputs).embeddings.squeeze(0).cpu().tolist()

        points.append(PointStruct(
            id=idx,
            vector=embedding,
            payload={
                "pdf_name": metadata["pdf_name"],
                "theme": metadata["theme"],
                "author": metadata["author"],
                "year": metadata["year"],
                "page": page
            }
        ))

    except Exception as e:
        print(f"❌ Error procesando {path.name}: {e}")

# Subir por lotes
for i in range(0, len(points), batch_size):
    client.upsert(collection_name=collection_name, points=points[i:i+batch_size])

print(f"✅ Embeddings subidos correctamente: {len(points)} imágenes.")
