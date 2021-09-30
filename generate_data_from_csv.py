import json
import pandas as pd
from pathlib import Path
import numpy as np

if __name__ == '__main__':
    manu_data_dir = Path.cwd()/'util'/'manuscripts.csv'

    #checking if the manuscript csv is available
    if (manu_data_dir.is_file()):
        manu_df = pd.read_csv(manu_data_dir, na_values=['Unidentified', 'N/A'])
    else:
        raise FileNotFoundError("Manuscript data file is missing")

    #only select the rows that are finished record
    manu_df = manu_df.head(24)

    #renaming columns
    manu_df.columns=['arab_title', 'chinese_title', 'people_involved', 'type', 'place', 'year', 'publisher', 'num_pages']

    #export each manuscript to an individual json file
    for i in manu_df.index:
        ind_manu_dir = Path.cwd()/'data'/'{}.json'.format(i)
        manu_df.loc[i].to_json(ind_manu_dir)


