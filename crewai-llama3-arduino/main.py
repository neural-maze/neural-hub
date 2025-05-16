from crewai import Crew
from dotenv import load_dotenv

from agents import sketch_programmer_agent, arduino_uploader_agent
from tasks import sketch_programming_task, arduino_uploading_task

load_dotenv()


crew = Crew(
            agents=[sketch_programmer_agent, arduino_uploader_agent],
            tasks=[sketch_programming_task, arduino_uploading_task],
        )

result = crew.kickoff()

print(result)
