from common.AgentsBot import AgentsBot, AgentsJob
import streamlit as st
import socket
import glob
import os


image_path = st.secrets.logo
results = ''
hostname = socket.gethostname()
openai_api_key = None
settings_disable = False

# load Default Job.
j = AgentsJob()
j.load_default_Job()
topic = None
topic_placeholder = j.config['topic']
agent1_role = j.config['agent1']['role']
agent1_goal = j.config['agent1']['goal']
agent1_backstory = j.config['agent1']['backstory']
agent2_role = j.config['agent2']['role']
agent2_goal = j.config['agent2']['goal']
agent2_backstory = j.config['agent2']['backstory']
task1_description = j.config['task1']['description']
task2_description = j.config['task2']['description']


st.title("🔎 Multiple Agents with search capability")
st.caption("🚀 A streamlit chatbot powered by CrewAI, OpenAI LLM and DuckDuckGo Search")

tab1, tab2, tab3 = st.tabs(["Bot", "Settings", "Archived Results"])

with st.sidebar:
    st.image(image_path, width=100) 
    openai_api_key = st.text_input("OpenAI API Key", key=openai_api_key, type="password")

    #options = ['Default', 'Research Program', 'Research News']
    option = st.selectbox('Select a crew agent',('Default', 'Research Program', 'Research News'))
    if option:
        if 'Program' in option:
            st.write('Loading Research Program')
            j.load_json_file('jobs/job_research_programs.json')
        elif 'News' in option:
            st.write('Loading News')
            j.load_json_file('jobs/job_research_news_today.json')
        else:
            st.write('Loading Default Program')
            j.load_default_Job()


with tab2:

    st.subheader('Job')
    st.write(option)

    st.subheader('Agent #1')
    agent1_role = st.text_input('Role', j.config['agent1']['role'], disabled = settings_disable)
    agent1_goal = st.text_area('Goal', j.config['agent1']['goal'], disabled = settings_disable)
    agent1_backstory = st.text_area('Backstory', j.config['agent1']['backstory'], disabled = settings_disable)
    
    st.subheader("Agent #2")
    agent2_role = st.text_input('Role', j.config['agent2']['role'], disabled = settings_disable)
    agent2_goal = st.text_area('Goal', j.config['agent2']['goal'], disabled = settings_disable)
    agent2_backstory = st.text_area('Backstory',agent2_backstory, disabled = settings_disable)
    
    st.subheader('Task #1')
    task1_description = st.text_area('Description',j.config['task1']['description'], disabled = settings_disable)
    
    st.subheader('Task #2')
    task2_description = st.text_area('Description',j.config['task2']['description'], disabled = settings_disable)

with tab3:
    directory_path = 'results'
    pattern = "*.md"
    files = glob.glob(os.path.join(directory_path, pattern))  # Use os.path.join for correct path construction
    content = '## Contents here ##'

    def show_contents(filename):
        with open(filename, "r") as file:
            content = file.read()
            return content

    st.header('Results')
    st.subheader('Click a file name to see the result')

    for filename in files:
        if st.button(filename):
            st.markdown(show_contents(filename))


## MAIN BODY OF PAGE ##
with tab1:
    st.subheader("Topic")
    topic = st.text_input('', placeholder=topic_placeholder)
    st.write(results)

    # if running from my local machine
    if 'Daniels-iMac.local' in hostname:
        openai_api_key = st.secrets.openai['key']

    # if running from codeshare
    if 'codeshare' in hostname:
        openai_api_key = st.secrets.openai['key']

    if st.button("Get Report"):

        if not openai_api_key:
            st.info("Please add your OpenAI API key to continue.")
            st.stop()

        if not topic:
            st.info("Please add your topic to continue.")
            st.stop()

        with st.spinner('Wait for it...'):

            c = AgentsBot(openai_api_key=openai_api_key)   
            j.config['topic'] = topic
            j.config['agent1']['role'] = agent1_role
            j.config['agent1']['goal'] = agent1_goal
            j.config['agent1']['backstory'] = agent1_backstory
            j.config['agent2']['role'] = agent2_role
            j.config['agent2']['goal'] = agent2_goal
            j.config['agent2']['backstory'] = agent2_backstory
            j.config['task1']['description'] = task1_description
            j.config['task2']['description'] = task2_description

            c.config = j.config
            crew_results = c.run()
            results = crew_results
            st.markdown(results)
    