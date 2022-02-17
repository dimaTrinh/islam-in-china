from fastapi import Request, APIRouter, Depends
from fastapi.templating import Jinja2Templates
from app.util.login import get_current_username

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/add_manuscript/")
async def add_manu(request: Request, username: str = Depends(get_current_username)):
    context = dict(
        request=request,
        title="Add Manuscript",
    )
    return templates.TemplateResponse("manu_add.html", context)
