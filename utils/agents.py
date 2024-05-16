from textwrap import dedent
from crewai import Agent
from langchain_community.llms import Ollama

# from tools import Tools

ollama_openhermes = Ollama(model="llama2")
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
    def extract_headings_agent(self):
        # tools = Tools()
        return Agent(
            role="Heading Extraction Agent",
            goal="Extract headings from the provided content",
            backstory="Extracts and returns only the headings from the provided markdown content.",
            verbose=True,
            llm=ollama_openhermes,
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
    