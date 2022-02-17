from fastapi import Request, APIRouter, Depends, UploadFile, File, Form
from fastapi.templating import Jinja2Templates
from app.util.login import get_current_username
from app.util.handle_data_from_csv import get_data_from_csv, write_data_to_csv
from app.util.models import get_data
import os
import pandas as pd

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

    # generate new row to be written to the csv file from the form
    new_manu_ind = str(get_data_from_csv(write_file=False) + 1)
    new_manu_id = "text_{}".format(new_manu_ind.zfill(3))
    new_row = [new_manu_id, arab_title, chinese_title, author, assembler, editor,
               scrivener, translator, type, place, publisher, year, stand_year, language,
               num_pages, description, notes]
    write_data_to_csv(new_row)

    # generate new data for the site and new manifest
    get_data_from_csv(write_file=True)

    manuscripts, idx_dict = get_data()
    context = dict(
        request=request,
        manuscripts=manuscripts,
        title='Manuscript List View'
    )
    return templates.TemplateResponse("manu_list.html", context)
