from pathlib import Path

import pandas as pd


def get_data_from_spreadsheet(write_file=False):  # whether we want to write new files to disk or not
    manu_data_dir = Path.cwd() / 'data' / 'spreadsheet' / 'pilot.xlsx'

    # checking if the manuscript csv is available
    if (manu_data_dir.is_file()):
        manu_df = pd.read_excel(manu_data_dir, na_values=['Unidentified', 'N/A'])
        manu_df.dropna(how="all", inplace=True)  # drop all empty lines
    else:
        raise FileNotFoundError("Manuscript file is missing")

    # renaming columns
    manu_df.columns = ['id', 'arab_title_script', 'arab_title', 'chinese_title', 'author', 'assembler', 'editor',
                       'scrivener', 'translator', 'type', 'place', 'publisher', 'year', 'stand_year', 'language',
                       'num_pages', 'description', 'notes']

    if write_file:
        # export each manuscript to an individual json file
        for i in manu_df.index:
            # the file is saved by their project ID
            ind_manu_dir = Path.cwd() / 'data' / 'metadata' / '{}.json'.format(manu_df.loc[i].id)
            manu_df.loc[i].to_json(ind_manu_dir)

    return len(manu_df.index)


def delete_data_from_spreadsheet(text_id):
    # read in existing data
    manu_data_dir = Path.cwd() / 'data' / 'spreadsheet' / 'pilot.xlsx'
    manu_df = pd.read_excel(manu_data_dir, na_values=['Unidentified', 'N/A'])
    manu_df.dropna(how="all", inplace=True)

    # delete the columns that have id the same as text_id
    manu_df = manu_df[manu_df.id != text_id]

    # write the new data to directory
    manu_df.to_excel(manu_data_dir, index=False)


def write_data_to_spreadsheet(new_row):
    # read in existing data
    manu_data_dir = Path.cwd() / 'data' / 'spreadsheet' / 'pilot.xlsx'
    manu_df = pd.read_excel(manu_data_dir, na_values=['Unidentified', 'N/A'])
    manu_df.dropna(how="all", inplace=True)

    # add in a new row to the dataframe
    manu_df.loc[len(manu_df.index)] = new_row

    # write the new data to directory
    manu_df.to_excel(manu_data_dir, index=False)


if __name__ == "__main__":
    get_data_from_spreadsheet(write_file=True)
