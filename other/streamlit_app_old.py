
import os
import google_auth_oauthlib.flow
from googleapiclient.discovery import build
import streamlit as st
import webbrowser
from openai import OpenAI
from dotenv import load_dotenv
import socket


load_dotenv()
OpenAI_key = os.environ.get("OPEN_AI_KEY")

fqdn = socket.getfqdn()
hostname = socket.gethostname()

redirect_uri = os.environ.get("REDIRECT_URI", "https://littleaibites-smyg87hdmugauhmn5t9yjq.streamlit.app/")
if 'codespaces' in hostname:
    redirect_uri = os.environ.get("REDIRECT_URI", "https://obscure-sniffle-x5x67wq5663vqrp-8501.app.github.dev/")

image_path = "littleaibites.png"  # Replace with the actual path

def main():
    if "google_auth_code" not in st.session_state:
        auth_flow()

    if "google_auth_code" in st.session_state:
        email = st.session_state["user_info"].get("email")
        st.write(f"Hello {email}")

        with st.sidebar:
            st.image(image_path)
            openai_api_key = st.text_input("OpenAI API Key", key=OpenAI_key, type="password")

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
