import logging
import os

from typing import Dict, List
from datetime import datetime
from fastapi import FastAPI, UploadFile

from models import UploadModel, FileModel
from database_manager import DatabaseManager
from database_manager.conditions import Conditions
from discord_client.discord_client import DiscordClient


logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

app = FastAPI()

CLIENT_TOKEN = os.environ.get('CLIENT_TOKEN')
CHANNEL_ID = int(os.environ.get('CHANNEL_ID'))


discord_client = DiscordClient()
discord_client.run_client(CLIENT_TOKEN)

database_manager = DatabaseManager()
database_manager.connect("diskord.db")


@app.get("/")
async def root() -> Dict[str, str]:
    logger.info("Test")
    return {"message": "Hello World"}


# @app.get("/hello/{name}")
# async def say_hello(name: str) -> Dict[str, str]:
#     return {"message": f"Hello {name}"}

def get_upload_urls(upload_id: int) -> List[str]:
    file_models = database_manager.select('files', FileModel, Conditions(upload_id=upload_id), row_limit=100)
    return [file_model.url for file_model in file_models]


@app.get("/upload/{upload_id}")
async def get_upload_files(upload_id: int) -> Dict[str, List[str]]:
    return {"urls": get_upload_urls(upload_id)}


@app.get("/collection/{collection_id}")
async def get_upload_files(collection_id: int) -> Dict[int, List[str]]:
    upload_models = database_manager.select('uploads', UploadModel, Conditions(collection_id=collection_id),
                                            row_limit=100)
    return {upload_model.id: get_upload_urls(upload_model.id) for upload_model in upload_models}


@app.post("/upload/")
async def create_upload_file(file: UploadFile) -> Dict[str, str]:
    logger.info(f"uploading {file.filename}")
    url = await discord_client.upload_file(file, CHANNEL_ID)
    upload = UploadModel(user_id='1', size=file.size, upload_time=datetime.now())
    result = database_manager.insert('uploads', upload)
    file_model = FileModel(url=url, upload_id=result.lastrowid)
    database_manager.insert('files', file_model)
    return {"url": url}
