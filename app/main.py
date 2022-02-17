from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Optional
import srsly
from pathlib import Path
from app.routers import add_manuscript
from app.util.models import Manuscript, get_data
import os

app = FastAPI()
app.mount("/assets", StaticFiles(directory="assets"), name="assets")
templates = Jinja2Templates(directory="templates")
app.include_router(add_manuscript.router)


# os.environ['TESTING'] = "-1"


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
async def page_manu_view(request: Request, manu_id: str):
    manuscripts, idx_dict = await get_data()
    context = dict(
        request=request,
        manu=manuscripts[idx_dict[manu_id]],
        title="Image Viewer for Manuscript",
    )
    return templates.TemplateResponse("image_viewer.html", context)


# landing page for individual manuscript
@app.get("/manuscripts/{manu_id}")
async def ind_manu_view(request: Request, manu_id: str):
    manuscripts, idx_dict = await get_data()
    context = dict(
        request=request,
        manu=manuscripts[idx_dict[manu_id]],
        title="Manuscript Individual View",
    )
    return templates.TemplateResponse("manu_view.html", context)


# list of all manuscripts
@app.get("/manuscripts/")
async def manu_list_view(request: Request):
    manuscripts, idx_dict = await get_data()
    context = dict(
        request=request,
        manuscripts=manuscripts,
        title='Manuscript List View'
    )
    return templates.TemplateResponse("manu_list.html", context)
