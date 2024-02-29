# Example from https://streamlit.io/generative-ai
from langchain.callbacks import StreamlitCallbackHandler
from langchain.agents import initialize_agent
from langchain.tools import DuckDuckGoSearchRun
from langchain.chat_models import ChatOpenAI
import streamlit as st

# if running from my local machine
if 'Daniels-iMac.local' in st.session_state.hostname:
    st.session_state.openai_api_key = st.secrets.openai['key']

# if running from codeshare
if 'codespaces' in st.session_state.hostname:
    st.session_state.openai_api_key = st.secrets.openai['key']
st.set_page_config(layout='wide')

with st.sidebar:
    # for locall development, create .streamlit folder with secreats.toml file
    image_path = st.secrets.logo
    st.image(image_path, width=100)

    if 'openai_api_key' in st.session_state:
        if st.session_state.openai_api_key == None:
            st.warning("Please add your OpenAI API key on the main page to continue.")
        else:
            st.info("OpenAI enabled")

    
st.title("🔎 Chat with search")
st.caption("🚀 A streamlit chatbot powered by OpenAI LLM and DuckDuckGo Search")

if "search_messages" not in st.session_state:
    st.session_state["search_messages"] = [
        {"role": "assistant", "content": "Hi, I'm a chatbot who can search the web. How can I help you?"}
    ]

for msg in st.session_state.search_messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input(placeholder="What is the latest news for today"):
    st.session_state.search_messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    if 'openai_api_key' in st.session_state:

        llm = ChatOpenAI(model_name="gpt-3.5-turbo", openai_api_key=st.session_state.openai_api_key, streaming=True)
        search = DuckDuckGoSearchRun(name="Search")
        search_agent = initialize_agent([search], llm, handle_parsing_errors=True) # , agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,

        with st.chat_message("assistant"):
            st_cb = StreamlitCallbackHandler(st.container(), expand_new_thoughts=False)
            response = search_agent.run(st.session_state.search_messages, callbacks=[st_cb])
            st.session_state.search_messages.append({"role": "assistant", "content": response})
            st.write(response)