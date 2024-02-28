
# https://pypi.org/project/StreamlitGAuth/2.0.9/
# https://docs.streamlit.io/streamlit-community-cloud/deploy-your-app/secrets-management
import os
import socket
import streamlit as st

# configuration
fqdn = socket.getfqdn()
hostname = socket.gethostname()

image_path = st.secrets.logo
openai_key = st.secrets.openai['key']
developer = st.secrets.email

def main():

    st.set_page_config(page_title="Little AI Bites", page_icon=None, layout="wide", initial_sidebar_state="auto")
    st.image(image_path, width=400)
    st.write("This Streamlit app shows how we can interact with multiple AI technologies")
    st.write('Debug - FQDN',fqdn)
    st.write('Debug - hostname',hostname)


if __name__ == "__main__":
    main()
# To run, type in terminal: streamlit run st_google_auth.py
