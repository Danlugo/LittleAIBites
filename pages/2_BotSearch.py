# Example from https://streamlit.io/generative-ai
from langchain.callbacks import StreamlitCallbackHandler
from langchain.agents import initialize_agent, AgentType
from langchain.tools import DuckDuckGoSearchRun
from langchain.chat_models import ChatOpenAI
import streamlit as st
import socket
import os

# if running from my local machine
hostname = socket.gethostname()
if 'Daniels-iMac.local' in hostname:
    openai_key = st.secrets.openai['key']

with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", key="langchain_search_api_key_openai", type="password")


st.title("🔎 Chat with search")
st.caption("🚀 A streamlit chatbot powered by OpenAI LLM and DuckDuckGo Search")

if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "Hi, I'm a chatbot who can search the web. How can I help you?"}
    ]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input(placeholder="What is the latest news for today"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    if openai_key:
        openai_api_key = openai_key

    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()

    llm = ChatOpenAI(model_name="gpt-3.5-turbo", openai_api_key=openai_api_key, streaming=True)
    search = DuckDuckGoSearchRun(name="Search")
    search_agent = initialize_agent([search], llm, handle_parsing_errors=True) # , agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,

    with st.chat_message("assistant"):
        st_cb = StreamlitCallbackHandler(st.container(), expand_new_thoughts=False)
        response = search_agent.run(st.session_state.messages, callbacks=[st_cb])
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.write(response)