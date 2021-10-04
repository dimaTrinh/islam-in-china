from fastapi import FastAPI, Request, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Json
from typing import Optional
import srsly
from pathlib import Path

app = FastAPI()
app.mount("/assets", StaticFiles(directory="assets"), name="assets")
templates = Jinja2Templates(directory="templates")


class Manuscript(BaseModel):
    arab_title: Optional[str]
    chinese_title: Optional[str]
    people_involved: Optional[str]
    type: Optional[str]
    place: Optional[str]
    year: Optional[str]
    publisher: Optional[str]
    num_pages: Optional[str]


def get_data():
    data_dir = Path.cwd() / 'data'
    manuscripts = []
    for item in data_dir.iterdir():
        data = srsly.read_json(item)
        if data:
            item = Manuscript(**data)
            manuscripts.append(item)
        else:
            raise FileNotFoundError("Manuscript data file is missing")
    return manuscripts


@app.route("/")
def index(request: Request):
    manuscripts = get_data()
    context = dict(
        request=request,
        manuscripts=manuscripts,
    )
    return templates.TemplateResponse("manu_list.html", context)
