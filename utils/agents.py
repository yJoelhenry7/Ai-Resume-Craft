from textwrap import dedent
from crewai import Agent


class Tasks():
    def data_create_agent(self):
        return Agent(
            role="",
            goal="",
            backstory=dedent(f"""\
            """),
            verbose=True,
            tools=[],
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
    