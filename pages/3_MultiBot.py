from common.AgentsBot import AgentsBot, AgentsJob
import streamlit as st
import socket
import glob
import os

# configuration
image_path = 'images/side_bar_bot_01.png'
results = ''
settings_disable = False
st.set_page_config(page_title="MultiBot", page_icon=None, layout="wide", initial_sidebar_state="expanded")

if not 'side_bar_image' in st.session_state:
    st.session_state.side_bar_image = image_path

if not 'openai_api_key' in st.session_state:
    st.session_state['openai_api_key'] = None

if not 'disable_functionality' in st.session_state:
    st.session_state['disable_functionality'] = True

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
st.warning(":bomb: !!!Please note that reports are saved and accessible in 'Archive Results' tab. Please DONT add text that are keys/passwords to it!!!")

tab1, tab2, tab3 = st.tabs(["Bot", "Settings", "Archived Results"])

with st.sidebar:
    st.image(image_path, width=100)

    if 'openai_api_key' in st.session_state:
        #st.write(st.session_state.openai_api_key)
        if not st.session_state.openai_api_key == None:
            if not st.session_state.openai_api_key == '':
                st.info("OpenAI enabled")
        else:
            st.warning("Please add your OpenAI API key on the main page to continue.")

    if 'disable_functionality' in st.session_state:
        st.write('Disabled', st.session_state.disable_functionality)
        pass

    #options = ['Default', 'Research Program', 'Research News']
    option = st.selectbox('Select a crew agent',('Default', 'Research Program', 'Research News', 'Company Profile'))
    if option:
        if 'Program' in option:
            st.write('Loading Template')
            j.load_json_file('jobs/job_research_programs.json')
        elif 'News' in option:
            st.write('Loading Template')
            j.load_json_file('jobs/job_research_news_today.json')
        elif 'Profile' in option:
            st.write('Loading Template')
            j.load_json_file('jobs/job_company_profile.json')            
        else:
            st.write('Loading Default Template')
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

    if st.session_state.openai_api_key:

        if st.button("Get Report"):

            if not topic:
                st.info("Please add topic to continue")
                st.stop()

            with st.spinner('Wait for it...'):

                try:
                    c = AgentsBot(openai_api_key=st.session_state.openai_api_key)   
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
                except Exception as e:
                    st.warning('There was an error. Please make sure API Key is valid', e)
                    pass
    