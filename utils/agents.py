import os 
from textwrap import dedent
from crewai import Agent
# from tools import Tools
from langchain_openai import ChatOpenAI

model = os.environ.get("OPENAI_MODEL_NAME")
base_url = os.environ.get("OPENAI_API_BASE")
llm = ChatOpenAI( model = model, base_url = base_url)



class Agents():
    # def extract_text_agent(self):
    #     tools = Tools()
    #     return Agent(
    #         role="Text Extraction Agent",
    #         goal="Extract Text from the provided file",
    #         backstory="Extracts and returns only the text from the provided file.",
    #         verbose=True,
    #         tools=tools.convert_md_tool("frames/resume.pdf"),
    #     )
    def extract_headings_agent(self,format):
        return Agent(
            role='Main Heading Extraction Agent',
            goal=f'Extract only the main headings for {format} from the provided content ',
            backstory=dedent("""
                Extracts and returns only the main headings (level 1 headings) from the provided markdown content.
            """),
            verbose=True,
            llm=llm,
            # tools=tools.convert_md_tool("frames/resume.pdf"),
        )
    
    def resume_create_agent(self):
        return Agent(
            role="",
            goal="",
            backstory=dedent(f"""\
            """),
            verbose=True,
            tools=[],
        )
    