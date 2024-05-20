from fastapi import APIRouter, Request,HTTPException,Form, UploadFile, File
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from crewai import Crew, Process
from utils.agents import Agents
from utils.tasks import Tasks
from utils.helpers import Helpers
# from utils.tools import Tools
from langchain_openai import ChatOpenAI
import os
from textwrap import dedent
import io
import re


model = os.environ.get("OPENAI_MODEL_NAME")
base_url = os.environ.get("OPENAI_API_BASE")
llm = ChatOpenAI( model = model, base_url = base_url)


router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    
    return templates.TemplateResponse("home.html", { "request" : request,"message":"" })


@router.post("/submit", response_class=HTMLResponse)
async def submit(request: Request, documentType: str = Form(...), fileUpload: UploadFile = File(...)):
    if documentType not in ["resume", "coverletter"]:
        raise HTTPException(status_code=400, detail="Invalid document type")

    if fileUpload.content_type not in ["application/pdf", "application/msword", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"]:
        raise HTTPException(status_code=400, detail="Invalid file type")

    # Process the file and document type as needed
    # Read file content
    content = await fileUpload.read()
    content_type = fileUpload.content_type
    
    frame_path = f'frames/{documentType}.pdf'
    helper = Helpers()
    frame_contents = helper.convert_pdf_to_md(frame_path)
    text_content = helper.extract_text_from_file(content,content_type)

    agent = Agents()
    headings_agent = agent.extract_headings_agent(documentType)
    segregate_agent = agent.segregate_content_agent()

    task = Tasks()
    headings_task = task.extract_headings_task(headings_agent, frame_contents,documentType)
    segregate_task = task.segregate_content_task(segregate_agent, text_content)


    segregate_task.context = [headings_task]
    crew = Crew(
        agents=[headings_agent, segregate_agent],
        tasks=[headings_task, segregate_task],
        llm=llm,
        verbose=2
    )

    # Get the Crew to work
    result = crew.kickoff()

    return templates.TemplateResponse("home.html", {"request": request, "message": f"Final Result : {result} "})
