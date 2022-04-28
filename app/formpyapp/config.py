import os

from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.environ["FLASK_SECRET"]

IMG_STORAGE_PATH = os.environ["IMG_STORAGE_PATH"]
DOCS_FOLDER_PATH = os.environ["DOCS_FOLDER_PATH"]

MONGODB_HOST = os.environ["MONGODB_HOSTNAME"]
MONGODB_PORT = int(os.environ["MONGODB_PORT"])
MONGODB_DATABASE = os.environ["MONGODB_DATABASE"]
# MONGODB_USERNAME = os.environ["MONGODB_USERNAME"]
# MONGODB_PASSWORD = os.environ["MONGODB_PASSWORD"]
