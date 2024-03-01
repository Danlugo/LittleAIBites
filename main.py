import os
import socket
import streamlit as st

# configuration
hostname = socket.gethostname()
image_path = 'images/side_bar_bot_01.png'
openai_api_key = None

if not 'side_bar_image' in st.session_state:
    st.session_state.side_bar_image = image_path

if not 'hostname' in st.session_state:
    st.session_state['hostname'] = hostname

if not 'openai_api_key' in st.session_state:
    st.session_state['openai_api_key'] = openai_api_key

if 'openai_api_key' in st.session_state:
    openai_api_key = st.session_state.openai_api_key

if not 'disable_functionality' in st.session_state:
    st.session_state['disable_functionality'] = True


st.set_page_config(page_title="Little AI Bites", page_icon=None, layout="wide", initial_sidebar_state="expanded")
st.image('images/header_02.png', width=1000)

st.markdown("""
# App
This is an streamlit demo app that showcases various AI bot usages in one place using a very lite UI framework that is easy to build and maintain.

## Pages
1. Bot : Showcases a generic chatbot like chatgpt or gemini (on text)
2. BotSearch: Like the Bot example but it has access to the internet thus it is more practical.
3. MultiBot: Combines the power of multiple AI agents talking to each other to accomplish a task. The agents also have access to the internet.
4. PDF Reader: Allows you to upload multiple PDF files and converse with them. Its a great demo for researching documents.

## Next
1. Will be adding more AI functionalities in the future to demostrate how we can use AI
2. Will continue to improve UI (Theme, Menus, etc)

### Usage
1. Please use the left sidebar to enter your API Keys to enable the functionality of all the bots.
""")

#st.write(hostname)

with st.sidebar:
    st.image(image_path, width=100)
    #st.write(openai_api_key)
    #st.write(st.session_state.openai_api_key)

    openai_api_key = st.text_input("Add OpenAI API Key and press enter", key=openai_api_key, placeholder='*************', type="password")
    if (openai_api_key != None):
        if (openai_api_key !=''):
            
            if(openai_api_key==st.secrets.developer):
                open_api_key = st.screts.openai.key

            st.session_state.openai_api_key = openai_api_key
            st.session_state['disable_functionality'] = False
            st.info('Key Added. Thanks')

    if st.session_state.openai_api_key != None:
        if st.session_state.openai_api_key != '':
            st.info('Key Added.')


    if 'disable_functionality' in st.session_state:
        st.write('Disabled', st.session_state.disable_functionality)
        pass