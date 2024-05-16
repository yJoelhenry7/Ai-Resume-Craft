from textwrap import dedent
from crewai import Task


class Tasks():
    def extract_headings_task(self,agent,output,format):
        return Task(
            description=dedent(f"""
                    Extract only main headings for {format} from the provided markdown content: {output} 
                """),
            expected_output=dedent("""
                    Extracted main headings in Markdown format
                """),
            agent=agent,
        )
    
    def resume_create_task(self,agent):
        return Task(
            description=dedent(f"""
                Segregate text from the provided PDF content into categories
            """),
            expected_output=dedent("""
                Text segregated into categories
            """),
            agent=agent,
        )
    
