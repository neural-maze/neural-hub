from pydantic import BaseModel

class TextInput(BaseModel):
    text: str
    
class SentimentOutput(BaseModel):
    label: str
    score: float
