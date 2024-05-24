from fastapi import APIRouter, Request, HTTPException, UploadFile, status,Response, Form, File, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from config.database import engine, Base, get_db
from utils.schemas import UserCreate, Token
from models.dbhelpers import create_user, get_user_by_username
from utils.auth import verify_password, create_access_token,get_current_user_by_token
from crewai import Crew, Process
from utils.agents import Agents
from utils.tasks import Tasks
from utils.helpers import Helpers
# from utils.tools import Tools
from langchain_openai import ChatOpenAI
import os


Base.metadata.create_all(bind=engine)


model = os.environ.get("OPENAI_MODEL_NAME")
base_url = os.environ.get("OPENAI_API_BASE")
llm = ChatOpenAI( model = model, base_url = base_url)


router = APIRouter()
templates = Jinja2Templates(directory="templates")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    
    return templates.TemplateResponse("home.html", { "request" : request,"message":"" })

@router.get("/signin",response_class=HTMLResponse)
async def signin(request: Request):
    return templates.TemplateResponse("signin.html",{ "request" : request,"message":"" })

@router.get("/signup",response_class=HTMLResponse)
async def signup(request: Request):
    return templates.TemplateResponse("signup.html",{ "request" : request,"message":"" })


@router.post("/signup", response_model=Token)
async def signup(response: Response, username: str = Form(...), password: str = Form(...), confirm_password: str = Form(...),  db: Session = Depends(get_db)):
    if password != confirm_password:
        raise HTTPException(status_code=400, detail="Passwords do not match")
    db_user = get_user_by_username(db, username=username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    user_create = UserCreate(username=username, password=password)
    data = create_user(db=db, user=user_create)
    access_token = create_access_token(data={"sub": data.username})
    response.set_cookie(key="access_token", value=access_token)
    response.set_cookie(key="user_name", value=data.username)
    return {"access_token": access_token, "token_type": "bearer","user_name": data.username}

@router.post("/token", response_model=Token)
async def login_for_access_token(response: Response, form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = get_user_by_username(db, username=form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.username})
    response.set_cookie(key="access_token", value=access_token)
    response.set_cookie(key="user_name", value=user.username)
    return {"access_token": access_token, "token_type": "bearer","user_name": user.username}

@router.get("/get_current_user")
async def get_current_user(response: Response,token: str,db: Session = Depends(get_db)):
    current_user = get_current_user_by_token(db,token)
    return current_user

@router.get("/user_selection", response_class=HTMLResponse)
async def user_selection(request: Request):
    return templates.TemplateResponse("user_selection.html", { "request" : request,"message":"" })


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
