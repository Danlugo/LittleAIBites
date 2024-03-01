from langchain_community.tools import DuckDuckGoSearchRun
from langchain_community.llms import Ollama
from langchain_openai import ChatOpenAI
from crewai import Agent, Task, Crew
from dotenv import load_dotenv
import datetime
import json
import os

class AgentsJob:

    def __init__(self) -> None:
        pass

    def load_job(self, job_dict):
        # load the dictionary objects into the config dictionary object
        self.config = job_dict


    def load_json_file(self, file_name):
        # load the json file values into a dictionary object
        with open(file_name, 'r') as f:
            data = f.read()
            self.config = json.loads(data)
            
    def load_default_Job(self):
        file_name = 'jobs/job_default.json'
        self.load_json_file(file_name)

class AgentsBot:
    """ 
    2024-02-22 - v0.01 - dgonzalez - created initial structure for crewai to read file for instructions
    2024-02-26 - v0.02 - dgonzalez - updated to be more generic and to use both json and dict obj as job inputs
    2024-02-27 - v0.03 - dgonzalez - updated the code so all is based on dictionary so it can be overriten on web app easier.
    """

    version = 0.02
    config = None
    search_tool = None
    agent_verbose = True
    crew_verbose = 2
    default_llm = None
    local_llm = None

    def __init__(self, openai_api_key) -> None:
        
        self.cloud_llm=ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.3, openai_api_key=openai_api_key)
        self.local_llm=Ollama(model="mistral")
        self.default_llm = self.cloud_llm
        self.search_tool = DuckDuckGoSearchRun()


    def load_default_Job(self):
        file_name = 'jobs/job_default.json'
        self.load_json_file(file_name)


    def save_markdown(self, content, filename_prefix="markdown"):
        # Get current date and time in YYYY-MM-DD_HH-MM-SS format
        now = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

        # Create the filename with timestamp
        filename = f"results/{now}_{filename_prefix}.md"

        # Save the content to the file
        with open(filename, "w") as file:
            file.write(content)

        return 'Saved Results'

    def load_job(self, job_dict):
        # load the dictionary objects into the config dictionary object
        self.config = job_dict


    def load_json_file(self, file_name):
        # load the json file values into a dictionary object
        with open(file_name, 'r') as f:
            data = f.read()
            self.config = json.loads(data)
            

    def run(self):
        agent1 = Agent(
            role = self.config['agent1']['role'].replace('#topic#',self.config['topic']),
            goal = self.config['agent1']['goal'].replace('#topic#',self.config['topic']),
            backstory = self.config['agent1']['backstory'].replace('#topic#',self.config['topic']),
            verbose=self.agent_verbose,
            allow_delegation=False,
            tools=[self.search_tool],
            max_iter=10,
            max_rpm=14
            )
    
        agent2 = Agent(
            role = self.config['agent2']['role'].replace('#topic#',self.config['topic']),
            goal = self.config['agent2']['goal'].replace('#topic#',self.config['topic']),
            backstory = self.config['agent2']['backstory'].replace('#topic#',self.config['topic']),
            verbose=self.agent_verbose,
            allow_delegation=True,
            max_iter=10,
            max_rpm=14      
            )

        task1 = Task( 
            description= self.config['task1']['description'].replace('#topic#',self.config['topic']), 
            agent=agent1, 
            expected_output=self.config['task1']['expected_output']
            )
        
        task2 = Task( 
            description= self.config['task2']['description'].replace('#topic#',self.config['topic']), 
            agent=agent2, 
            expected_output=self.config['task2']['expected_output']
            )

        crew = Crew(
            agents=[agent1, agent2],
            tasks=[task1, task2],
            verbose=self.crew_verbose,
            manager_llm=self.default_llm
            )

        results = crew.kickoff()
        self.save_markdown(results)

        return results
    
    def printify(self):
        print(json.dumps(self.config, indent=4).replace('#topic#', self.config['topic']))

    def __str__(self):
        return str(self.config)


if __name__ == "__main__":
    load_dotenv(dotenv_path='.streamlit/.env')
    openai_api_key = os.environ.get('OPENAI_API_KEY')
    c = AgentsBot(openai_api_key)
    c.load_json_file('jobs/job_research_programs.json')
    c.printify()
    j = c.run()
    print('\nRESULTS:\n',j)