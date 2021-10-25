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
    index: Optional[int]
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
    idxDict = {}  # map the real index of the manuscript to the index in the list above
    for (index, item) in enumerate(data_dir.iterdir()):
        data = srsly.read_json(item)
        if data:
            item = Manuscript(**data)
            manuscripts.append(item)
            idxDict[item.index] = index
        else:
            raise FileNotFoundError("Manuscript data file is missing")
    return manuscripts, idxDict


# index page
@app.get("/")
async def index(request: Request):
    context = dict(
        request=request,
    )
    return templates.TemplateResponse("base.html", context)


# image viewer for each manuscript
@app.get("/manuscript_view/{manu_id}")
async def page_manu_view(request: Request, manu_id: int):
    context = dict(
        request=request,
        title="Image Viewer for Manuscript",
    )
    return templates.TemplateResponse("image_viewer.html", context)


# landing page for individual manuscript
@app.get("/manuscripts/{manu_id}")
async def ind_manu_view(request: Request, manu_id: int):
    manuscripts, idxDict = get_data()
    context = dict(
        request=request,
        manu=manuscripts[idxDict[manu_id]],
        title="Manuscript Individual View",
    )
    return templates.TemplateResponse("manu_view.html", context)


# list of all manuscripts
@app.get("/manuscripts/")
async def manu_list_view(request: Request):
    manuscripts, idxDict = get_data()
    context = dict(
        request=request,
        manuscripts=manuscripts,
        title='Manuscript List View'
    )
    return templates.TemplateResponse("manu_list.html", context)
