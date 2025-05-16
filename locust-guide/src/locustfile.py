import json
import os
import random

from locust import HttpUser, constant_pacing, task


def load_json_file(file_path: str):
    with open(file_path, 'r') as file:
        data = json.load(file)
        return data
    
COMMENTS = load_json_file(
    os.path.join(os.path.dirname(__file__), "data/example_comments.json")
)

class LoadTestSentiment(HttpUser):    
    wait_time = constant_pacing(1)
    
    @task
    def post_sentiment(self):
        comment = random.choice(COMMENTS)
        self.client.post("/predict-sentiment", json=comment)
