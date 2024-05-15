from textwrap import dedent
from crewai import Task


class Tasks():
    def data_create_task(self,agent):
        return Task(
            description = dedent(f"""\
            """),
            expected_output=dedent(f"""\
            """),
            agent=agent
        )
    
    def resume_create_task(self,agent):
        return Task(
            description = dedent(f"""\
            """),
            expected_output=dedent(f"""\
            """),
            agent=agent
        )
    
