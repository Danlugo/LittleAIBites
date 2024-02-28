import os
import socket
from common.AgentsBot import AgentsBot
import streamlit as st
import json

image_path = st.secrets.logo
results = 'Results will be displayed here'
fqdn = socket.getfqdn()
hostname = socket.gethostname()
openai_api_key = None
openai_key = None
settings_disable = True

# if running from my local machine
if 'Daniels-iMac.local' in hostname:
    openai_key = st.secrets.openai['key']

c = AgentsBot()
c.load_default_Job()
topic = None
topic_placeholder = c.config['topic']
agent1_role = c.config['agent1']['role']
agent1_goal = c.config['agent1']['goal']
agent1_backstory = c.config['agent1']['backstory']
agent2_role = c.config['agent2']['role']
agent2_goal = c.config['agent2']['goal']
agent2_backstory = c.config['agent2']['backstory']
task1_description = c.config['task1']['description']
task2_description = c.config['task2']['description']


st.title("Research Bot")

tab1, tab2 = st.tabs(["Bot", "Settings"])

with st.sidebar:
    st.image(image_path, width=100) 

    openai_api_key = st.text_input("OpenAI API Key", key=openai_key, type="password")



with tab2:

    st.subheader('Agent #1')
    agent1_role = st.text_input('Role', agent1_role, disabled = settings_disable)
    agent1_goal = st.text_area('Goal', agent1_goal, disabled = settings_disable)
    agent1_backstory = st.text_area('Backstory', agent1_backstory, disabled = settings_disable)
    
    st.subheader("Agent #2")
    agent2_role = st.text_input('Role', agent2_role, disabled = settings_disable)
    agent2_goal = st.text_area('Goal',agent2_goal, disabled = settings_disable)
    agent2_backstory = st.text_area('Backstory',agent2_backstory, disabled = settings_disable)
    
    st.subheader('Task #1')
    task1_description = st.text_area('Description',task1_description, disabled = settings_disable)
    
    st.subheader('Task #2')
    task2_description = st.text_area('Description',task2_description, disabled = settings_disable)

## MAIN BODY OF PAGE ##
with tab1:
    st.subheader("Topic")
    topic = st.text_input('Topic', placeholder=topic_placeholder)
    st.write(results)
    if st.button("Get Report"):
        if not openai_api_key:
            if not openai_key:
                st.info("Please add your OpenAI API key to continue.")
                st.stop()
            else:
                    openai_api_key = openai_key

            if not topic:
                st.info("Please add your topic to continue.")
                st.stop()

        # override user passed settings
        c.config['topic'] = topic
        c.config['agent1']['role'] = agent1_role
        c.config['agent1']['goal'] = agent1_goal
        c.config['agent1']['backstory'] = agent1_backstory
        c.config['agent2']['role'] = agent2_role
        c.config['agent2']['goal'] = agent2_goal
        c.config['agent2']['backstory'] = agent2_backstory
        c.config['task1']['description'] = task1_description
        c.config['task2']['description'] = task2_description

        c.api_key=openai_api_key
        crew_results = c.run()
        results = crew_results

        st.markdown(results)
    