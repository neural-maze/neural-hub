import json
from PIL import Image
import streamlit as st

from crew import MelodyCrew


LOGO = Image.open("./img/logo.png")


st.set_page_config(page_title="Melody Agents", layout="centered", page_icon=LOGO)


with st.sidebar:
    st.image(LOGO)
    st.markdown("---")
    st.markdown(
        "# How to use\n"
        "1. Think of any topic you want (e.g. 'The last discussion between Yann Lecun and Elon Musk')\n\n"
        "2. Pick a music genre (e.g. 'Hip Hop', 'Rap', 'Heavy Metal')\n\n"
        "3. Click 'Submit' and let the agents work 😄\n\n"
    )
    st.markdown(
        "# About\n"
        "**Melody Agents** is a PoC that explores the connection between crewAI and Suno AI."
        "The project works like this: \n\n"
        "1. One agent conducts a **web research** about the topic provided, fetching all the "
        " relevant information\n\n"
        "2. Another agent will generate high quality lyrics based on the web research. The lyrics"
        " will be adapted to the specific **genre**.\n\n"
        "3. The last agent, using a custom tool, will send the lyrics into Suno AI to generate"
        " two songs."
    )

st.markdown("<h1 style='text-align: center;'>🎺 Melody Agents 🎸</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center;'>When crewAI meets Suno AI</h4>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center;'>🎵 🎼 🎶 🎵 🎼 🎶 🎵 🎼 🎶</h4>", unsafe_allow_html=True)
st.markdown("---")

topic = st.text_area("Provide a topic: ", height=2, value="")
genre = st.text_area("Provide music genre: ", height=2, value="")

st.markdown("---")


if st.button("Submit"):
    if not (topic and genre):
        st.warning("You need to provide a Topic and a Music Genre!!")
    else:
        with st.spinner("Agents are working ... "):
            melody_crew = MelodyCrew(topic, genre)
            result = melody_crew.run()
            
            st.markdown("Your songs are being generated!! Please go to your Suno account and enjoy the melody!! 🤖🤖🤖 \n\n ")
