import os
from crewai import Agent, Task, Crew, Process
from dotenv import load_dotenv
from langchain_community.llms import Ollama
from langchain_openai import ChatOpenAI
from langchain_community.tools import DuckDuckGoSearchRun
import json


class ConversationalBot:
    """ 
    created on 2024-02-22 - v0.1 - dgonzalez - initial structure for crewai to read file for instructions
    """

    version = 0.01
    config = None
    search_tool = None
    agent_verbose = True
    crew_verbose = 2
    default_llm = None
    local_llm = None

    def __init__(self, filename) -> None:

        load_dotenv()
        self.default_llm=ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.7)
        self.local_llm=Ollama(model="mistral")
        self.config = self.load_json_file(filename)
        self.topic = self.config['topic']
        self.researcher = self.config['researcher']
        self.writer = self.config['writer']
        self.task1 = self.config['task1']['description'].replace('#topic#',self.topic)
        self.task2 = self.config['task2']['description'].replace('#topic#',self.topic)
        
        self.search_tool = DuckDuckGoSearchRun()
         
    def load_json_file(self, filename):
        with open(filename, 'r') as f:
            data = f.read()
        return json.loads(data)

    def run(self):
        researcher = Agent(
            role = self.researcher['role'].replace('#topic#',self.topic),
            goal = self.researcher['goal'].replace('#topic#',self.topic),
            backstory = self.researcher['backstory'].replace('#topic#',self.topic),
            verbose=self.agent_verbose,
            allow_delegation=False,
            tools=[self.search_tool],
            #llm=default_llm
            )
    
        writer = Agent(
            role = self.researcher['role'].replace('#topic#',self.topic),
            goal = self.researcher['goal'].replace('#topic#',self.topic),
            backstory = self.researcher['backstory'].replace('#topic#',self.topic),
            verbose=self.agent_verbose,
            allow_delegation=True,
            #llm=default_llm
            )

        task1 = Task( description= self.task1, agent=researcher)

        task2 = Task( description= self.task2, agent=writer)

        crew = Crew( agents=[researcher, writer],tasks=[task1, task2],verbose=self.crew_verbose )

        return crew.kickoff()
    
    def printify(self):
        print(json.dumps(self.config, indent=4).replace('#topic#', self.topic))

    def __str__(self):
        return str(self.config)


if __name__ == "__main__":
    c = ConversationalBot('job_LLS_Technical_Education.json')
    c.printify()
    j = c.run()
    print('\nRESULTS:\n',j)