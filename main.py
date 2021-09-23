from fastapi import FastAPI, Request, HTTPException
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Json
import json

app = FastAPI()

templates = Jinja2Templates(directory="templates")