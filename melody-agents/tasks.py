from crewai import Task
from textwrap import dedent
from agents import MelodyAgents
from crewai import Agent


class MelodyTasks:
    def web_research_task(self, agent: Agent, topic: str):
        return Task(
                description=dedent(f"""
                    Conduct a web research about the next topic:
                    
                    ```
                    {topic}
                    ```
                    
                    Your final answer must be a detailed report about the 
                    topic, gathering all relevant information and details 
                    about it
                    """),
                expected_output=dedent("A detailed report of the topic"),
                agent=agent)
        
    def lyrics_creation_task(self, agent: Agent, topic: str, genre: str):
        return Task(
            description=dedent("""
                Create high quality lyrics for a {genre} song about the next topic:
                
                ```
                {topic}
                ```
                
                Use the information gathered by the previous agent and adapt the
                writing style to following music: {genre}. 
                
                Your final answer must be the lyrics of the song, and nothing else. 
                """),
            expected_output="The lyrics of the song, and nothing else",
            agent=agent
        )
    
    def song_generation_task(self, agent: Agent):
        return Task(
            description="Generate a song from the provided lyrics",
            expected_output="Show the user the urls for checking the generated songs",
            agent=agent
        )
