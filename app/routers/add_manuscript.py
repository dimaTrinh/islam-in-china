from fastapi import Request, APIRouter, Depends, UploadFile, File, Form
from fastapi.templating import Jinja2Templates
from app.util.login import get_current_username
from app.util.handle_data_from_csv import get_data_from_csv, write_data_to_csv
from app.util.models import get_data
from app.util.convert_pdf_to_images import pdf_to_images
from app.util.generate_manifest_from_json import generate_ind_manifest
from app.util.save_images_to_disk import save_images
from typing import List

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
                      stand_year: int = Form(0),
                      language: str = Form(None),
                      description: str = Form(None),
                      notes: str = Form(None),
                      image_files: List[UploadFile] = Form(...),
                      ):
    # get the index for the new text
    new_manu_ind = str(await get_data_from_csv(write_file=False) + 1)

    # get the internal id we use for manuscript file
    new_manu_id = "text_{}".format(new_manu_ind.zfill(3))

    # process and save the images to disk
    num_pages, image_name_dict = await save_images(new_manu_id, image_files)

    # generate new row to be written to the csv file from the form
    new_row = [new_manu_id, arab_title, chinese_title, author, assembler, editor,
               scrivener, translator, type, place, publisher, year, stand_year, language,
               num_pages, description, notes]
    await write_data_to_csv(new_row)

    # generate the new metadata for the site along with its manifest
    await get_data_from_csv(write_file=True)
    await generate_ind_manifest(new_manu_id, num_pages, image_name_dict)

    manuscripts, idx_dict = await get_data()
    context = dict(
        request=request,
        manuscripts=manuscripts,
        title='Manuscript List View'
    )
    return templates.TemplateResponse("manu_list.html", context)
