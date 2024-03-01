import os
import socket
import streamlit as st
from openai import OpenAI

# Configuration
image_path = 'images/side_bar_bot_01.png'
st.set_page_config(page_title="Bot", page_icon=None, layout="wide", initial_sidebar_state="expanded")

if not 'side_bar_image' in st.session_state:
    st.session_state.side_bar_image = image_path

if not 'openai_api_key' in st.session_state:
    st.session_state['openai_api_key'] = None

if not 'disable_functionality' in st.session_state:
    st.session_state['disable_functionality'] = True

with st.sidebar:
    # for locall development, create .streamlit folder with secreats.toml file    
    st.image(image_path, width=100)

    if 'openai_api_key' in st.session_state:
        
        if not st.session_state.openai_api_key == None:
            if not st.session_state.openai_api_key == '':
                st.info("OpenAI enabled")
        else:
            st.warning("Please add your OpenAI API key on the main page to continue.")
                
    if 'disable_functionality' in st.session_state:
        st.write('Disabled', st.session_state.disable_functionality)
        pass

st.title("💬 Chatbot")
st.caption("🚀 A streamlit chatbot powered by OpenAI LLM")

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input(disabled=st.session_state['disable_functionality']):

    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    try:
        client = OpenAI(api_key=st.session_state.openai_api_key)
        response = client.chat.completions.create(model="gpt-3.5-turbo", messages=st.session_state.messages)
        msg = response.choices[0].message.content
        st.session_state.messages.append({"role": "assistant", "content": msg})
        st.chat_message("assistant").write(msg)
    except Exception as e:
        st.warning('There was an error. Make sure API key is valid')
        pass
    
    