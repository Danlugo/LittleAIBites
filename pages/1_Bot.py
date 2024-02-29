import os
import socket
import streamlit as st
from openai import OpenAI

# configuration
openai_api_key = None

# if running from my local machine
if 'Daniels-iMac.local' in st.session_state.hostname:
    st.session_state.openai_api_key = st.secrets.openai['key']

# if running from codeshare codespaces
if 'codespaces' not in st.session_state.hostname:
    st.session_state.openai_api_key = st.secrets.openai['key']
st.set_page_config(layout='wide')

with st.sidebar:
    # for locall development, create .streamlit folder with secreats.toml file
    image_path = st.secrets.logo
    st.image(image_path, width=100)

    if 'openai_api_key' in st.session_state:
        #st.write(st.session_state.openai_api_key)
        if st.session_state.openai_api_key == None:
            st.warning("Please add your OpenAI API key on the main page to continue.")
        else:
            st.info("OpenAI enabled")

    if 'disable_functionality' in st.session_state:
        #st.write('Disabled', st.session_state.disable_functionality)
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

    client = OpenAI(api_key=st.session_state.openai_api_key)
    
    response = client.chat.completions.create(model="gpt-3.5-turbo", messages=st.session_state.messages)
    
    msg = response.choices[0].message.content
    
    st.session_state.messages.append({"role": "assistant", "content": msg})
    
    st.chat_message("assistant").write(msg)