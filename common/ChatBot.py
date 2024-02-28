import os
import socket
import streamlit as st
from openai import OpenAI


class ChatBot:
    """
    created on 2024-02-25 - dgonzalez - initial structure. 
    TODO: Complete code
    
    """

    version = 0.1
    api_key = None

    def __init__(self) -> None:
        
        fqdn = socket.getfqdn()
        hostname = socket.gethostname()
        openai_api_key = st.secrets.openai['key']
        pass