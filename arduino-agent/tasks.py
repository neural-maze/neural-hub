from textwrap import dedent

from crewai import Task

from agents import sketch_programmer_agent, arduino_uploader_agent

sketch_programming_task = Task(
    description=dedent(
        "Write a Sketch script that can be immediately uploaded to an Arduino. Just the Arduino code, nothing else."),
    expected_output=dedent("A plain Sketch script that can be copy and pasted directly into the Arduino CLI"),
    agent=sketch_programmer_agent,
    output_file="./tmp/tmp.ino",
)

arduino_uploading_task = Task(
    description=dedent(
        "Compile and Upload the the Sketch script into the Arduino"),
    expected_output=dedent("Just compile the code and upload it into the Arduino"),
    agent=arduino_uploader_agent,
)

