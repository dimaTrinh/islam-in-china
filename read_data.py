import json
import pandas as pd
from pathlib import Path
import numpy as np

if __name__ == '__main__':
    manu_data_dir = Path.cwd()/'util'/'manuscripts.csv'
    if (manu_data_dir.is_file()):
        manu_df = pd.read_csv(manu_data_dir, na_values=['Unidentified'])
    else:
        raise FileNotFoundError("Manuscript data file is missing")
    manu_df = manu_df.head(24)
    print(manu_df)

