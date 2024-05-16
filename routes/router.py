from fastapi import APIRouter
from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
# from utils.tools import Tools  
from crewai import Crew, Process
from utils.agents import Agents
from utils.tasks import Tasks
from utils.helpers import Helpers
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
    
    pdf_file_path = 'frames/resume.pdf'
    helper = Helpers()
    file_contents = helper.convert_pdf_to_md(pdf_file_path)

    agent = Agents()
    headings_agent = agent.extract_headings_agent('resume')

    task = Tasks()
    headings_task = task.extract_headings_task(headings_agent, file_contents,'resume')

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
