from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/")
async def index(request: Request):
    context = {"request": request, "root-route": "http://127.0.0.1:8000"}
    return templates.TemplateResponse("index.html", context)


@app.post("/request_answer")
async def return_answer(request: dict) -> dict:
    print(request)
    return {"message": "Answer!"}
