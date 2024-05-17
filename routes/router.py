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
from textwrap import dedent


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
    my_doc = dedent("""
        John Doe is a highly skilled and innovative software developer with over a decade of experience in designing, developing, and deploying software solutions across various industries. With a strong foundation in computer science and a passion for continuous learning, John has consistently delivered high-quality software that meets the ever-evolving needs of his clients and employers. His expertise spans multiple programming languages, development frameworks, and project management methodologies, making him a versatile and valuable asset to any development team. Throughout his career, John has demonstrated a commitment to excellence, an ability to adapt to new technologies, and a collaborative spirit. He has led the development of cloud-based CRM systems, architected microservices-based applications, and mentored junior developers, significantly enhancing team productivity. His technical skills include proficiency in JavaScript, Python, Java, and Swift, along with extensive experience in web and backend development, cloud services, and DevOps tools. John holds a Bachelor of Science in Computer Science from the University of TechVille, along with certifications like Certified ScrumMaster and AWS Certified Solutions Architect. He actively contributes to open-source projects, writes a tech blog, and participates in hackathons, reflecting his dedication to staying at the forefront of the tech industry. John's ability to deliver impactful software solutions, coupled with his collaborative approach and commitment to mentorship, makes him an invaluable member of any development team.
    """)

    agent = Agents()
    headings_agent = agent.extract_headings_agent('resume')
    segregate_agent = agent.segregate_content_agent()

    task = Tasks()
    headings_task = task.extract_headings_task(headings_agent, file_contents,'resume')
    segregate_task = task.segregate_content_task(segregate_agent, my_doc)


    segregate_task.context = [headings_task]

    crew = Crew(
    agents=[headings_agent, segregate_agent],
    tasks=[headings_task, segregate_task],
    llm=llm,
    verbose=2
    )

    # Get the Crew to work
    result = crew.kickoff()

    # print("######################")
    # print(result)
    return templates.TemplateResponse("home.html", { "request" : request,"message":result })
