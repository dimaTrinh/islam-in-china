from typing import List

from fastapi import Request, APIRouter, Depends, UploadFile, Form
from fastapi.templating import Jinja2Templates

from app.util.generate_manifest_from_json import generate_ind_manifest
from app.util.handle_data_from_spreadsheet import get_data_from_spreadsheet, write_data_to_spreadsheet
from app.util.login import get_current_username
from app.util.models import get_data
from app.util.save_images_to_disk import save_images

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
                      arab_title_script: str = Form(...),
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
                      num_pages: int = Form(0),
                      description: str = Form(None),
                      notes: str = Form(None),
                      image_files: List[UploadFile] = Form(...),
                      ):
    # get the index for the new text
    new_manu_ind = get_data_from_spreadsheet(write_file=False)
    new_manu_ind += 1

    # get the internal id we use for manuscript file
    new_manu_id = "text_{}".format(str(new_manu_ind).zfill(3))

    # process and save the images to disk
    # return the number of pages uploaded and a dictionary of the files
    num_pages_up, image_name_dict = await save_images(new_manu_id, image_files)

    # generate new row to be written to the csv file from the form
    new_row = [new_manu_id, arab_title_script, arab_title, chinese_title, author, assembler, editor,
               scrivener, translator, type, place, publisher, year, stand_year, language,
               num_pages, description, notes]
    write_data_to_spreadsheet(new_row)

    # generate the new metadata for the site along with its manifest
    get_data_from_spreadsheet(write_file=True)
    generate_ind_manifest(new_manu_id, num_pages_up, image_name_dict)

    manuscripts, idx_dict = get_data()
    context = dict(
        request=request,
        manuscripts=manuscripts,
        title='Manuscript List View'
    )
    return templates.TemplateResponse("manu_list.html", context)
