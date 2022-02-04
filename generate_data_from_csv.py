import json
import pandas as pd
from pathlib import Path
import numpy as np

if __name__ == '__main__':
    manu_data_dir = Path.cwd() / 'util' / 'pilot_manuscript.csv'

    # checking if the manuscript csv is available
    if (manu_data_dir.is_file()):
        manu_df = pd.read_csv(manu_data_dir, na_values=['Unidentified', 'N/A'])
    else:
        raise FileNotFoundError("Manuscript file is missing")

    # only select the rows that are finished record
    manu_df = manu_df.head(4)

    # renaming columns
    manu_df.columns = ['id', 'arab_title', 'chinese_title', 'author', 'assembler', 'editor',
                       'scrivener', 'translator', 'type', 'place', 'publisher', 'year', 'stand_year', 'language',
                       'num_pages', 'description', 'notes']
    # export each manuscript to an individual json file
    for i in manu_df.index:
        # the file is saved by their project ID
        ind_manu_dir = Path.cwd() / 'data' / '{}.json'.format(manu_df.loc[i].id)
        manu_df.loc[i].to_json(ind_manu_dir)
