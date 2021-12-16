from iiif_prezi.factory import ManifestFactory
from pathlib import Path, PurePath
import json

# refer to https://github.com/iiif-prezi/iiif-prezi/blob/master/CODE_WALKTHROUGH.md
# https://github.com/iiif-prezi/iiif-prezi/blob/master/examples/build-from-directory.py

fac = ManifestFactory()
image_dir = Path.cwd() / 'assets' / 'img' / 'texts'
pre_zir = "/tmp"

# Where the resources live on the web
fac.set_base_prezi_uri("http://167.99.0.192:8000/iiif/2/")
# Where the resources live on disk
fac.set_base_prezi_dir("./assets/img/texts/")

# Default Image API information
fac.set_base_image_uri("http://167.99.0.192:8000/iiif/2/")
fac.set_iiif_image_info(2.0, 2)  # Version, ComplianceLevel

fac.set_debug("warn")

data_dir = Path.cwd() / 'data'

img_dict = {}  # dictionary that maps a manuscript id with the images in the manuscript

for img in image_dir.iterdir():
    # getting manuscript name from image file
    manu_name = PurePath(img).parts[-1].split('_page')[0]
    
    #get page number and remove leading 0
    pg_number = int(PurePath(img).parts[-1].split('page_')[-1].split('.')[0].lstrip("0"))
    if manu_name not in img_dict: #create a dictionary that maps page number to the right image
        img_dict[manu_name] = {}
    img_dict[manu_name][pg_number] = img

for (index, item) in enumerate(data_dir.iterdir()):
    # extract the id of the manuscript from the directory path
    manu_name = PurePath(item).parts[-1].split('.')[0]
    print("Building manuscript for {}".format(manu_name))

    # setting up the manifest
    manifest = fac.manifest(ident="identifier/{}".format(manu_name),
                            label="Manifest for {}".format(manu_name))
    manifest.viewingDirection = "left-to-right"
    seq = manifest.sequence()

    for page in range(1, len(img_dict[manu_name])+1):
        # extract identity from image's name
        ident = PurePath(img_dict[manu_name][page]).parts[-1]
        #get page number
        title = 'Page ' + ident.split('page_')[-1].split('.')[0]
        cvs = seq.canvas(ident=ident, label=title)
        cvs.set_image_annotation(ident, iiif=True)

    mfst = manifest.toJSON(top=True)

    manifest_dir = Path.cwd() / 'assets' / 'manifests' / '{}.json'.format(manu_name)
    with open(manifest_dir, 'w') as outfile:
        json.dump(mfst, outfile)
