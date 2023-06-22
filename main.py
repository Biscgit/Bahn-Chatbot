import asyncio

from fastapi import FastAPI, Request
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/favicon.ico")
async def favicon():
    return FileResponse("static/images/chat_icon.ico", media_type="image/x-icon")


@app.get("/")
async def index(request: Request):
    context = {"request": request, "rootroute": "http://127.0.0.1:8000"}
    return templates.TemplateResponse("index.html", context)


@app.post("/request_answer")
async def return_answer(request: dict) -> dict:
    print(request)
    await asyncio.sleep(2)
    return {"message": "Answer!"}
