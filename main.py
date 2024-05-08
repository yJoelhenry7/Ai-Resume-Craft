from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from routes.router import router

app = FastAPI()
app.mount("/static",StaticFiles(directory="static"),name="static")

# including the routes from router
app.include_router(router)
