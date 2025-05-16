import time
import json
import requests
from typing import Type
from pydantic.v1 import BaseModel, Field
from crewai_tools import BaseTool


class SunoToolSchema(BaseModel):
    """Input for SunoTool"""
    url: str = Field(..., description="URL for the Suno API. This field is mandatory")
    genre: str = Field(..., description="The song genre. E.g. Hip Hop, Rap, Pop, etc.")
    

class SunoTool(BaseTool):
    name: str = "Generate a song from the lyrics"
    description: str = "A tool that can be used to generate a song from the provided lyrics."
    args_schema: Type[BaseModel] = SunoToolSchema
    url: str = ""
    genre: str = ""
    
    def __init__(self, url: str, genre: str, **kwargs):
        super().__init__(**kwargs)
        self.url = f"{url}/api/custom_generate"
        self.genre = genre
        
    def _run(
        self,
        lyrics: str,
        **kwargs
    ):
        payload = {
            "prompt": lyrics,
            "tags": self.genre,
            "title": "Melody Agents Song",
            "make_instrumental": False,
            "wait_audio": False
        }
        try:
            response = requests.post(self.url, json=payload, headers={'Content-Type': 'application/json'})
            _ = response.json()
        except Exception as e:
            raise ValueError(e)
        
        return "Your songs are being generated ... 🤖"
