from fastapi import Request, APIRouter, Depends, UploadFile, File, Form
from fastapi.templating import Jinja2Templates
from app.util.login import get_current_username

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/add_manuscript/")
async def get_add_manu_form(request: Request, username: str = Depends(get_current_username)):
    context = dict(
        request=request,
        title="Add Manuscript",
    )
    return templates.TemplateResponse("manu_add.html", context)


@router.post("/add_manu_form")
async def handle_form(request: Request,
                      arab_title: str = Form(...),
                      chinese_title: str = Form(None),
                      author: str = Form(None),
                      assembler: str = Form(None),
                      editor: str = Form(None),
                      scrivener: str = Form(None),
                      translator: str = Form(None),
                      type: str = Form(None),
                      place: str = Form(None),
                      publisher: str = Form(None),
                      year: str = Form(None),
                      stand_year: int = Form(None),
                      language: str = Form(None),
                      num_pages: int = Form(...),
                      description: str = Form(None),
                      notes: str = Form(None),
                      manu_file: UploadFile = File(...)):
    manu_content = await manu_file.read()
    print(manu_file.filename)
    context = dict(
        request=request,
        title="Add Manuscript",
    )
    return templates.TemplateResponse("manu_add.html", context)
