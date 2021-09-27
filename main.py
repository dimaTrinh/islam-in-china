from fastapi import FastAPI, Request, HTTPException
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Json
import json

app = FastAPI()

templates = Jinja2Templates(directory="templates")

@app.route("/")
def index(request: Request):
    context = dict(
        request = request,
        my_string = "Wheeeee!",
        my_list = [0, 1, 2, 3, 4, 5],
    )
    return templates.TemplateResponse("manu_list.html", context)