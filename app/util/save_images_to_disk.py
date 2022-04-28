import os
import re
from pathlib import Path

import aiofiles


async def save_images(text_id, image_files):
    # get the image names, page number, and content of the image files from the uploaded file
    images = []
    for file in image_files:
        # remove the extension of the image to get image name
        file_name = os.path.splitext(file.filename)[0]

        # match any numbers at the end of the file name then remove leading 0 to get page number
        pg_number = int(re.search(r'[0-9]+$', file_name.strip()).group().lstrip('0'))

        # add to our list of images
        images.append([pg_number, file_name, await file.read()])

    # sort the images by the page number
    images.sort(key=lambda x: x[0])

    # save each page to the asset folder
    # a dictionary that maps the images stored on disk to the original uploaded file names
    image_name_dict = {}
    for (index, (pg, name, image_content)) in enumerate(images):
        pg_number = str(index + 1).zfill(3)
        image_id = '{}_page_{}.jpg'.format(text_id, pg_number)
        image_dir = Path.cwd() / 'assets' / 'img' / 'texts' / image_id
        async with aiofiles.open(image_dir, 'wb') as out_file:
            await out_file.write(image_content)
        image_name_dict[image_id] = name

    num_pages = len(images)

    return num_pages, image_name_dict
