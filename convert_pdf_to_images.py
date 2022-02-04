from pdf2image import convert_from_path
from pathlib import Path, PurePath

# reference: https://www.geeksforgeeks.org/convert-pdf-to-image-using-python/
# directory that contains all the PDFs of the manuscripts
pdf_dir = Path.cwd() / 'assets' / 'manuscript_pdf'

for manu_pdf in pdf_dir.iterdir():
    # extracting the name of the manuscript
    manu_name = PurePath(manu_pdf).parts[-1].split('.')[0]
    print("Converting {} into images".format(manu_name))

    # store pdf with convert_from_path function
    images = convert_from_path(manu_pdf, 600)
    print("Document has {} images".format(len(images)))

    for i in range(0, len(images)):
        # append leading zeroes to the page number
        pg_number = str(i + 1).zfill(3)

        # save each page to the asset folder
        image_dir = Path.cwd() / 'assets' / 'img' / 'texts' / '{}_page_{}.jpg'.format(manu_name, pg_number)
        images[i].save(image_dir, 'JPEG')
