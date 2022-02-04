from pdf2image import convert_from_path
from pathlib import Path, PurePath

pdf_dir = Path.cwd() / 'assets' / 'manuscript_pdf'

for img in pdf_dir.iterdir():
    if img.is_file():
        manu_name = PurePath(img).parts[-1].split('_Page')[0]
        pg_number = PurePath(img).parts[-1].split('Page_')[-1].split('.')[0]
        new_file = '{}_page_{}.jpg'.format(manu_name, pg_number)
        img.rename(pdf_dir / new_file)
