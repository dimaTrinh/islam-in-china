from pathlib import Path
import shutil

if __name__ == "__main__":
    text_id = "text_006"
    image_dir = Path.cwd() / 'data' / 'unprocessed_img' / text_id
    output_dir = Path.cwd() / 'assets' / 'img' / 'texts'

    for (ind, file) in enumerate(image_dir.iterdir()):

        for (ind, file) in enumerate(image_dir.iterdir()):
            pg_number = str(ind + 1).zfill(3)
            img_name = '{}_page_{}.jpg'.format(text_id, pg_number)
            output_path = output_dir / img_name
            print(img_name)
            shutil.copy(file, output_path)
