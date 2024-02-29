# Example from https://streamlit.io/generative-ai
from langchain.callbacks import StreamlitCallbackHandler
from langchain.agents import initialize_agent
from langchain.tools import DuckDuckGoSearchRun
from langchain.chat_models import ChatOpenAI
import streamlit as st

st.set_page_config(layout='wide')

with st.sidebar:
    # for locall development, create .streamlit folder with secreats.toml file
    image_path = st.secrets.logo
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