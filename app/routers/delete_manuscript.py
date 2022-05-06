from fastapi import Request, APIRouter, Depends, Form
from fastapi.templating import Jinja2Templates

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
    manuscripts, idx_dict = get_data()
    context = dict(
        request=request,
        manuscripts=manuscripts,
        title="Delete Manuscript",
    )
    return templates.TemplateResponse("manu_delete.html", context)
