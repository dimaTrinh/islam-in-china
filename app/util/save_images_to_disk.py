import os
import aiofiles
from pathlib import Path


async def save_images(text_id, image_files):
    # get the image names and the content of the image files from the uploaded file
    # remove the extension of the image
    images = [(os.path.splitext(file.filename)[0], await file.read()) for file in image_files]

    # sort the images alphabetically by file name
    images.sort(key=lambda x: x[0])

    # save each page to the asset folder
    # a dictionary that maps the images stored on disk to the original uploaded file names
    image_name_dict = {}
    for (index, (name, image_content)) in enumerate(images):
        pg_number = str(index + 1).zfill(3)
        image_id = '{}_page_{}.jpg'.format(text_id, pg_number)
        image_dir = Path.cwd() / 'assets' / 'img' / 'texts' / image_id
        async with aiofiles.open(image_dir, 'wb') as out_file:
            await out_file.write(image_content)
        image_name_dict[image_id] = name

    num_pages = len(images)

    return num_pages, image_name_dict
