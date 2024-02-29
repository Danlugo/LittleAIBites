import os
import socket
import streamlit as st

# configuration
hostname = socket.gethostname()
image_path = st.secrets.logo
openai_api_key = None

if not 'hostname' in st.session_state:
    st.session_state['hostname'] = hostname

if not 'openai_api_key' in st.session_state:
    st.session_state['openai_api_key'] = openai_api_key

if 'openai_api_key' in st.session_state:
    openai_api_key = st.session_state.openai_api_key

if not 'disable_functionality' in st.session_state:
    st.session_state['disable_functionality'] = True


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
st.write(hostname)

with st.sidebar:
    openai_api_key = st.text_input("Please add your OpenAI API Key so all pages demo work", key=openai_api_key, placeholder='*************' type="password")
    if openai_api_key:
        st.session_state['openai_api_key'] = openai_api_key
        st.session_state['disable_functionality'] = False
        st.info('Key Added. Thanks')

    if st.session_state.openai_api_key:
        st.info('Key Added.')


