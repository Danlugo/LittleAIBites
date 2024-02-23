import os
from crewai import Agent, Task, Crew, Process
from dotenv import load_dotenv
from langchain_community.llms import Ollama
from langchain_openai import ChatOpenAI
from langchain_community.tools import DuckDuckGoSearchRun



load_dotenv()
#default_llm=llm=ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.7) #Ollama(model="mistral")
search_tool = DuckDuckGoSearchRun()

topic = 'Give me the best in class of technology education programs for high school students'

# Define your agents with roles and goals
researcher = Agent(
  role='Senior Research Analyst',
  goal=f'Research: {topic}',
  backstory= f"""You work at a leading technology education company.
  Your expertise lies in finding the most accurate information tech education programs , in this case you will be researching: "'{topic}'".
  You have a knack for dissecting complex data and presenting actionable insights.""",
  verbose=True,
  allow_delegation=False,
  tools=[search_tool],
  #llm=default_llm
)


writer = Agent(
  role='Strategist writer',
  goal= f"Craft compelling content about '{topic}'",
  backstory="""You are a renowned tech educator , known for your insightful and engaging articles.
  You transform complex concepts into compelling narratives.""",
  verbose=True,
  allow_delegation=True,
  #llm=default_llm
)


# Create tasks for your agents
task1 = Task(
  description= f"""Conduct a comprehensive analysis for the {topic}.
  Check top 10 technology programs for high schoolers to find out what are the top emegenging technologies
  For each of the technology program found, collect what is included, how long is the program and how much it cost
  Check which one is the one that is most likely be successful and why
  Your final answer MUST be a full analysis report
  """,
  agent=researcher
)

task2 = Task(
  description= f"""Using the insights provided, develop an engaging document that highlights for {topic}.
  Your document should be informative yet accessible, catering to audiences insterested in using the company services.
  It should include the Summary at the top 
  Then for each program, provide a high level summary alogn with the program topics included and why they are needed.
  Make it sound professional, avoid complex words so it doesn't sound like AI.
  Your final answer MUST be the full document with summary and supporting articles""",
  agent=writer
)



# Instantiate your crew with a sequential process
crew = Crew(
  agents=[researcher, writer],
  tasks=[task1, task2],
  verbose=2, # You can set it to 1 or 2 to different logging levels
)

# Get your crew to work!
result = crew.kickoff()

print("######################")
print(result)