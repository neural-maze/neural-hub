import os
from textwrap import dedent
from dotenv import load_dotenv

from crewai import Crew
from langchain_groq import ChatGroq

from agents import MelodyAgents
from tasks import MelodyTasks

load_dotenv()


class MelodyCrew:
    
    # Change the URL if you are using another port
    URL = "http://suno-api:3000"
    LLM = ChatGroq(api_key=os.environ.get("GROQ_API_KEY"), model="llama3-70b-8192")

    
    def __init__(self, topic: str, genre: str):
        self.topic = topic
        self.genre = genre
        
    def run(self):
        agents = MelodyAgents(url=self.URL, genre=self.genre, llm=self.LLM)
        tasks = MelodyTasks()
        
        web_researcher_agent = agents.web_researcher_agent()
        lyrics_creator_agent = agents.lyrics_creator_agent()
        song_generator_agent = agents.song_generator_agent()
        
        web_research_task = tasks.web_research_task(
            agent=web_researcher_agent, 
            topic=self.topic
        )
        lyrics_creation_task = tasks.lyrics_creation_task(
            agent=lyrics_creator_agent, 
            topic=self.topic, 
            genre=self.genre
        )
        song_generation_task = tasks.song_generation_task(
            agent=song_generator_agent
        )
        
        crew = Crew(
            agents=[
                web_researcher_agent,
                lyrics_creator_agent,
                song_generator_agent
            ],
            tasks=[
                web_research_task,
                lyrics_creation_task,
                song_generation_task
            ],
        )
                
        return crew.kickoff()
