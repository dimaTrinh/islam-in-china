from typing import List
from typing import Optional

from fastapi import Request


# reference: https://www.fastapitutorial.com/blog/fastapi-jinja-create-job-post/

class ManuscriptForm:
    def __init__(self, request: Request):
        self.request: Request = request
        self.arab_title: Optional[str] = None
        self.chinese_title: Optional[str] = None
        self.author: Optional[str] = None
        self.assembler: Optional[str] = None
        self.editor: Optional[str] = None
        self.scrivener: Optional[str] = None
        self.translator: Optional[str] = None
        self.type: Optional[str] = None
        self.place: Optional[str] = None
        self.publisher: Optional[str] = None
        self.year: Optional[str] = None
        self.stand_year: Optional[int] = None
        self.language: Optional[str] = None
        self.num_pages: Optional[int] = None
        self.description: Optional[str] = None
        self.notes: Optional[str] = None

    async def load_data(self):
        form = await self.request.form()
        self.arab_title = form.get("arab_title")
        self.chinese_title = form.get("chinese_title")
        self.author = form.get("author")
        self.assembler = form.get("assembler")
        self.editor = form.get("editor")
        self.scrivener = form.get("scrivener")
        self.translator = form.get("translator")
        self.type = form.get("type")
        self.place = form.get("place")
        self.publisher = form.get("publisher")
        self.year = form.get("year")
        self.stand_year = form.get("stand_year")
        self.language = form.get("language")
        self.num_pages = form.get("num_pages")
        self.description = form.get("description")
        self.notes = form.get("notes")
