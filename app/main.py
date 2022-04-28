from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.routers import add_manuscript
from app.util.models import get_data

app = FastAPI()
app.mount("/assets", StaticFiles(directory="assets"), name="assets")
app.mount("/data", StaticFiles(directory="data"), name="data")
templates = Jinja2Templates(directory="templates")
app.include_router(add_manuscript.router)


# os.environ['TESTING'] = "-1"


# index page
@app.get("/")
async def index(request: Request):
    context = dict(
        request=request,
        title="Islam in China",
    )
    return templates.TemplateResponse("index.html", context)


# image viewer for each manuscript
@app.get("/manuscript_view/{manu_id}")
async def page_manu_view(request: Request, manu_id: str):
    manuscripts, idx_dict = get_data()
    context = dict(
        request=request,
        manu=manuscripts[idx_dict[manu_id]],
        title="Image Viewer for Manuscript",
    )
    return templates.TemplateResponse("image_viewer.html", context)


# landing page for individual manuscript
@app.get("/manuscripts/{manu_id}")
async def ind_manu_view(request: Request, manu_id: str):
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


# history page for Uyghur Community
@app.get("/history_islam/")
async def history_islam_view(request: Request):
    context = dict(
        request=request,
        title="History",
    )
    return templates.TemplateResponse("history_islam.html", context)


# history page for manuscripts
@app.get("/history_manu/")
async def history_manu_view(request: Request):
    context = dict(
        request=request,
        title="History",
    )
    return templates.TemplateResponse("history_manu.html", context)


# About Us Page
@app.get("/about_us/")
async def about_us_view(request: Request):
    context = dict(
        request=request,
        title="About Us",
    )
    return templates.TemplateResponse("about_us.html", context)


# contact page, currently blank
@app.get("/contact/")
async def contact_view(request: Request):
    context = dict(
        request=request,
        title="Contact",
    )
    return templates.TemplateResponse("contact.html", context)
