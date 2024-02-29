
# https://pypi.org/project/StreamlitGAuth/2.0.9/
# https://docs.streamlit.io/streamlit-community-cloud/deploy-your-app/secrets-management
import os
import socket
import streamlit as st
from openai import OpenAI

# configuration
fqdn = socket.getfqdn()
hostname = socket.gethostname()
openai_api_key = None
openai_key = None

# if running from my local machine
if 'Daniels-iMac.local' in hostname:
    openai_key = st.secrets.openai['key']



st.set_page_config(layout='wide')

with st.sidebar:
    # for locall development, create .streamlit folder with secreats.toml file
    image_path = st.secrets.logo
    st.image(image_path, width=100)
    openai_api_key = st.text_input("OpenAI API Key", key=openai_key, type="password")

st.title("💬 Chatbot")
st.caption("🚀 A streamlit chatbot powered by OpenAI LLM")

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    if not openai_api_key:
        if not openai_key:
            st.info("Please add your OpenAI API key to continue.")
            st.stop()
        else:
            openai_api_key = openai_key

    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    client = OpenAI(api_key=openai_api_key)
    
    response = client.chat.completions.create(model="gpt-3.5-turbo", messages=st.session_state.messages)
    
    msg = response.choices[0].message.content
    
    st.session_state.messages.append({"role": "assistant", "content": msg})
    
    st.chat_message("assistant").write(msg)