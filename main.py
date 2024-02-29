import os
import socket
import streamlit as st

# configuration
hostname = socket.gethostname()
image_path = st.secrets.logo


st.set_page_config(page_title="Little AI Bites", page_icon=None, layout="wide", initial_sidebar_state="auto")
st.image(image_path, width=200)

st.markdown("""
# App Contains:
This streamlit demo app aims at providing various AI bot usages in one place.

## Pages:
1. Bot : Showcases a generic chatbot like chatgpt or gemini (on text)
2. BotSearch: Like the Bot example but it has access to the internet thus it is more practical.
3. MultiBot: Combines the power of multiple AI agents talking to each other to accomplish a task. The agents also have access to the internet.
4. PDF Reader: Allows you to upload multiple PDF files and converse with them. Its a great demo for researching documents.

## Next:
1. Will be adding more AI functionalities in the future to demostrate how we can use AI
2. Will continue to improve UI (Theme, Menus, etc)

""")
st.write('Debug - hostname',hostname)