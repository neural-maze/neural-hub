import os
from textwrap import dedent

from crewai import Agent
from langchain_openai import ChatOpenAI

from tools.arduino import CompileAndUploadToArduinoTool

tool = CompileAndUploadToArduinoTool(
    ino_file_dir="./tmp",
    board_fqbn="arduino:avr:uno",
    port="/dev/cu.usbmodem1201"
)

llama3 = ChatOpenAI(
    model="llama3",
    base_url="http://localhost:11434/v1")
openai_llm = ChatOpenAI(api_key=os.environ.get("OPENAI_API_KEY"), model="gpt-3.5-turbo-0125")


sketch_programmer_agent = Agent(
    role="Sketch Programmer",
    goal=dedent(
        """Write a Sketch script for Arduino that lights a red led in digital pin 11, 
        a blue led in digital pin 10 and a green led in digital pin 9 with a time
        between the three of 1 second."""),
    backstory=dedent(
        """
        You are an experienced Sketch programmer who really enjoys programming Arduinos
        """
    ),
    verbose=True,
    allow_delegation=False,
    llm=llama3,
)

arduino_uploader_agent = Agent(
    role="Arduino Uploader Agent",
    goal="Your goal is to compile and upload the received arduino script using a tool",
    backstory=dedent(
        """
        You are a hardware geek.
        """
    ),
    verbose=True,
    allow_delegation=False,
    tools=[tool]
)
