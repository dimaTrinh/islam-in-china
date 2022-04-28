from pathlib import Path

from pdf2image import convert_from_bytes


# reference:  https://pdf2image.readthedocs.io/en/latest/overview.html

async def pdf_to_images(pdf_file, text_id):
    images = convert_from_bytes(pdf_file)

    for i in range(0, len(images)):
        # append leading zeroes to the page number
        pg_number = str(i + 1).zfill(3)
        # save each page to the asset folder
        image_dir = Path.cwd() / 'assets' / 'img' / 'texts' / '{}_page_{}.jpg'.format(text_id, pg_number)
        images[i].save(image_dir, 'JPEG')

    return (len(images))
