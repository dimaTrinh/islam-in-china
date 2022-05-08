from fastapi import Request, APIRouter, Depends, Form
from fastapi.templating import Jinja2Templates
from pathlib import Path

from app.util.login import get_current_username
from app.util.models import get_data
from app.util.handle_data_from_spreadsheet import delete_data_from_spreadsheet

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/delete_manuscript/")
async def get_delete_manu(request: Request, username: str = Depends(get_current_username)):
    manuscripts, idx_dict = get_data()
    context = dict(
        request=request,
        manuscripts=manuscripts,
        title="Delete Manuscript",
    )
    return templates.TemplateResponse("manu_delete.html", context)


@router.get("/delete_manuscript/{text_id}")
async def delete_manu(request: Request, text_id: str):
    # delete the manuscript from the spreadsheet
    delete_data_from_spreadsheet(text_id)

    # delete all images that start with the text_id
    image_dir = Path.cwd() / 'assets' / 'img' / 'texts'
    for file in image_dir.glob('{}*'.format(text_id)):
        file.unlink()

    # delete the json files that have the the text_id
    data_dir = Path.cwd() / 'data'
    for file in data_dir.rglob('{}.json'.format(text_id)):
        file.unlink()

    # refresh the data then return back to the delete manuscript site
    manuscripts, idx_dict = get_data()
    context = dict(
        request=request,
        manuscripts=manuscripts,
        title="Delete Manuscript",
    )
    return templates.TemplateResponse("manu_delete.html", context)
