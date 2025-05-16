from fastapi import FastAPI, HTTPException
from .schemas import TextInput, SentimentOutput

from transformers import pipeline

from functools import lru_cache


@lru_cache(maxsize=1)
def get_sentiment_analyzer():
    """Initialize and cache the sentiment analysis pipeline"""
    return pipeline("sentiment-analysis")

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "This is an example API"}

@app.post("/predict-sentiment")
async def predict_sentiment(input: TextInput) -> SentimentOutput:
    try: 
        sentiment_analyzer = get_sentiment_analyzer()
        result = sentiment_analyzer(input.text)
        sentiment = result[0]
        return SentimentOutput(
            label=sentiment["label"],
            score=sentiment["score"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error processing request") from e
