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
            async_execution=True,
            agent=agent,
        )
    
    def segregate_content_task(self,agent,text):
        return Task(
            description=f'Segregate text into categories from the provided markdown content: {text}',
            expected_output='Text segregated into categories',
            async_execution=False,
            agent=agent,
        )
    
