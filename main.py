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
    id: Optional[str]
    arab_title: Optional[str]
    chinese_title: Optional[str]
    author: Optional[str]
    assembler: Optional[str]
    editor: Optional[str]
    scrivener: Optional[str]
    translator: Optional[str]
    type: Optional[str]
    place: Optional[str]
    publisher: Optional[str]
    year: Optional[str]
    stand_year: Optional[int]
    language: Optional[str]
    num_pages: Optional[int]
    description: Optional[str]
    notes: Optional[str]


def get_data():
    data_dir = Path.cwd() / 'data'
    manuscripts = []  # list of manuscripts
    idx_dict = {}  # map the id of the manuscript to the index in the list above
    for (index, item) in enumerate(data_dir.iterdir()):
        data = srsly.read_json(item)
        if data:
            item = Manuscript(**data)
            manuscripts.append(item)
            idx_dict[item.index] = index
        else:
            raise FileNotFoundError("Manuscript old_data file is missing")
    return manuscripts, idx_dict


# index page
@app.get("/")
async def index(request: Request):
    context = dict(
        request=request,
        title="Landing Page",
    )
    return templates.TemplateResponse("index.html", context)


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
    manuscripts, idx_dict = get_data()
    context = dict(
        request=request,
        manu=manuscripts[idx_dict[manu_id]],
        title="Manuscript Individual View",
    )
    return templates.TemplateResponse("manu_view.html", context)


# list of all manuscripts
@app.get("/manuscripts/")
async def manu_list_view(request: Request):
    manuscripts, idx_dict = get_data()
    context = dict(
        request=request,
        manuscripts=manuscripts,
        title='Manuscript List View'
    )
    return templates.TemplateResponse("manu_list.html", context)
