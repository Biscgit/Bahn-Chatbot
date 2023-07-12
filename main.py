from fastapi import FastAPI, Request
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn

from app.source.chat import Chat

app = FastAPI()
app.mount("/public", StaticFiles(directory="public"), name="public")
templates = Jinja2Templates(directory="templates")

chats: dict[int, Chat] = {}


@app.get("/favicon.ico")
def website_icon():
    return FileResponse("public/images/chat_icon.ico", media_type="image/x-icon")


@app.get("/")
def index(request: Request):
    context = {"request": request, "rootroute": "http://127.0.0.1:8000"}
    return templates.TemplateResponse("index.html", context)


@app.post("/request_answer")
def return_answer(request: dict) -> dict:
    """Answering requests with data from unique chats"""
    user_id = request.get("user_id")

    chat = chats.get(user_id, Chat(user_id))
    message = request.get("message")

    response = chat.chatbot_response(message)
    chats.update({user_id: chat})

    return {"message": response}


if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8000)
