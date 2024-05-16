from fastapi import APIRouter
from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
# from utils.tools import Tools  
from crewai import Crew, Process
from utils.agents import Agents
from utils.tasks import Tasks
# from utils.tools import Tools
from langchain_openai import ChatOpenAI
import os
model = os.environ.get("OPENAI_MODEL_NAME")
base_url = os.environ.get("OPENAI_API_BASE")
llm = ChatOpenAI( model = model, base_url = base_url)


router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    message = "Hello"
    # tools = Tools()
    # res = tools.convert_md_tool("frames/resume.pdf")
    # Define the file path
    file_path = 'frames/resume.md'

    # Read the file and store its contents in a variable
    with open(file_path, 'r', encoding='utf-8') as file:
        file_contents = file.read()
    
    agent = Agents()
    headings_agent = agent.extract_headings_agent()

    task = Tasks()
    headings_task = task.extract_headings_task(headings_agent, file_contents)

    crew = Crew(
    agents=[headings_agent],
    tasks=[headings_task],
    llm=llm,
    verbose=2
    )

    # Get the Crew to work
    result = crew.kickoff()

    # print("######################")
    # print(result)
    return templates.TemplateResponse("home.html", { "request" : request,"message":result })
