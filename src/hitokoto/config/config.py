import os
from os.path import dirname, join

from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), ".env")
load_dotenv(dotenv_path)


class Config:
    SA_KEY_PATH = os.environ.get("SA_KEY_PATH")
    SPREADSHEET_ID = os.environ.get("SPREADSHEET_ID")
