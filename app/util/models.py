from pydantic import BaseModel
from typing import Optional
from pathlib import Path
import srsly


class Manuscript(BaseModel):
    id: Optional[str]
    arab_title_script: Optional[str]
    arab_title: Optional[str]
    chinese_title: Optional[str]
    author: Optional[str]
    assembler: Optional[str]
    editor: Optional[str]
    scrivener: Optional[str]
    translator: Optional[str]
    type: Optional[str]
    place: Optional[str]
    publisher: Optional[str]
    year: Optional[str]
    stand_year: Optional[int]
    language: Optional[str]
    num_pages: Optional[int]
    description: Optional[str]
    notes: Optional[str]


def get_data():
    data_dir = Path() / 'data' / 'metadata'
    manuscripts = []  # list of manuscripts
    idx_dict = {}  # map the id of the manuscript to the index in the list above
    for (index, item) in enumerate(data_dir.iterdir()):
        data = srsly.read_json(item)
        if data:
            item = Manuscript(**data)
            manuscripts.append(item)
            idx_dict[item.id] = index
        else:
            raise FileNotFoundError("Manuscript old_data file is missing")
    return manuscripts, idx_dict
