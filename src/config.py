import logging
import os
from dotenv import load_dotenv


logging.basicConfig(
    format="%(asctime)s - %(message)s", datefmt="%d-%b-%y %H:%M:%S", level=logging.INFO
)
logger = logging.getLogger()


load_dotenv()


DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")


SITE_URL = (
    "https://github.com/EvanLi/Github-Ranking/blob/master/Top100/Top-100-stars.md"
)
