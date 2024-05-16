from textwrap import dedent
from crewai import Task


class Tasks():
    def extract_headings_task(self,agent,output):
        return Task(
            description =dedent(f"""\
            Extract headings from the provided markdown content: {output}
            """),
            expected_output=dedent(f"""\ 
            Extracted headings in Markdown format'
            """),
            agent=agent,
        )
    
    def resume_create_task(self,agent):
        return Task(
            description = dedent(f"""\
            """),
            expected_output=dedent(f"""\
            """),
            agent=agent
        )
    
