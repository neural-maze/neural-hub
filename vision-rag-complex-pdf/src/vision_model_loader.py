import os
import torch
from transformers import ColQwen2ForRetrieval, ColQwen2Processor
from transformers.utils.import_utils import is_flash_attn_2_available
from dotenv import load_dotenv

load_dotenv("colqwen_qdrant_meetup/.env")

_colqwen_model = None
_colqwen_processor = None

COLQWEN_MODEL = os.getenv("COLQWEN_MODEL")

device = "cuda" if torch.cuda.is_available() else "cpu"

def get_colqwen_model():
    global _colqwen_model
    if _colqwen_model is None:
        _colqwen_model = ColQwen2ForRetrieval.from_pretrained(
            COLQWEN_MODEL,
            torch_dtype=torch.bfloat16,
            device_map=device,
            attn_implementation="flash_attention_2" if is_flash_attn_2_available() else "sdpa", 
            )
    return _colqwen_model

def get_colqwen_processor():
    global _colqwen_processor
    if _colqwen_processor is None:
        _colqwen_processor = ColQwen2Processor.from_pretrained(
            COLQWEN_MODEL,
            device_map=device
        )
    return _colqwen_processor