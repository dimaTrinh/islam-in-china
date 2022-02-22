import os
import aiofiles
from pathlib import Path


async def save_images(text_id, image_files):
    # get the image names and the content of the image files from the uploaded file
    # remove the extension of the image
    images = [(os.path.splitext(file.filename)[0], await file.read()) for file in image_files]

    # sort the images alphabetically by file name
    images.sort()

    # save each page to the asset folder
    for (index, (name, image_content)) in enumerate(images):
        pg_number = str(index + 1).zfill(3)
        image_dir = Path.cwd() / 'assets' / 'img' / 'texts' / '{}_page_{}.jpg'.format(text_id, pg_number)
        async with aiofiles.open(image_dir, 'wb') as out_file:
            await out_file.write(image_content)
            
    num_pages = len(images)

    return num_pages
