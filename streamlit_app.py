
# https://pypi.org/project/StreamlitGAuth/2.0.9/
# https://docs.streamlit.io/streamlit-community-cloud/deploy-your-app/secrets-management
import socket
import streamlit as st
from openai import OpenAI
from GoogleAuth import GoogleAuth


# configuration
fqdn = socket.getfqdn()
hostname = socket.gethostname()
image_path = st.secrets.logo
openai_key = st.secrets.openai['key']
developer = st.secrets.email


def main():
    st.set_page_config(layout='wide')

    g = GoogleAuth()

    if "google_auth_code" not in st.session_state:
        g.auth_flow()
        
    if "google_auth_code" in st.session_state:
        email = st.session_state["user_info"].get("email")
        st.write(f"Hello {email}")

        with st.sidebar:
            st.image(image_path)
            openai_api_key = st.text_input("OpenAI API Key", key=openai_key, type="password")
            if developer in email:
                openai_api_key = openai_key

        st.title("💬 Chatbot")
        st.caption("🚀 A streamlit chatbot powered by OpenAI LLM")

        if "messages" not in st.session_state:
            st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

        for msg in st.session_state.messages:
            st.chat_message(msg["role"]).write(msg["content"])

        if prompt := st.chat_input():
            if not openai_api_key:
                st.info("Please add your OpenAI API key to continue.")
                st.stop()

            client = OpenAI(api_key=openai_api_key)
            st.session_state.messages.append({"role": "user", "content": prompt})
            st.chat_message("user").write(prompt)
            response = client.chat.completions.create(model="gpt-3.5-turbo", messages=st.session_state.messages)
            msg = response.choices[0].message.content
            st.session_state.messages.append({"role": "assistant", "content": msg})
            st.chat_message("assistant").write(msg)


if __name__ == "__main__":
    main()
# To run, type in terminal: streamlit run st_google_auth.py
