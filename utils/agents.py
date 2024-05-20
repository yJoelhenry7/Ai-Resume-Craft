import os 
from textwrap import dedent
from crewai import Agent
# from tools import Tools
from langchain_openai import ChatOpenAI

model = os.environ.get("OPENAI_MODEL_NAME")
base_url = os.environ.get("OPENAI_API_BASE")
llm = ChatOpenAI( model = model, base_url = base_url)



class Agents():

    def extract_headings_agent(self,format):
        return Agent(
            role='Main Heading Extraction Agent',
            goal=f'Extract only the main headings for {format} from the provided content ',
            backstory=dedent(f"""
                Extracts and returns only the main headings (level 1 headings) for {format} from the provided markdown content.
            """),
            verbose=True,
            llm=llm,
            allow_delegation=False
        )
    
    def segregate_content_agent(self):
        return Agent(
            role='Text Segregation Agent',
            goal='Segregate text into categories',
            backstory='Organizes text into predefined categories in markdown format based on its content.',
            verbose=True,
            llm=llm,
            allow_delegation=False
        )
    