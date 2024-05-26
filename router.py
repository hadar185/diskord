import os
import logging

from typing import Dict, List
from datetime import datetime
from fastapi import FastAPI, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from utils import split_file, delete_file
from models import UploadModel, FileModel
from database_manager import DatabaseManager
from database_manager.conditions import Conditions
from discord_client.discord_client import DiscordClient

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

app = FastAPI()

origins = [
    "http://localhost:8081",
    "http://10.100.102.15:8081"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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


async def get_upload_urls(upload_id: int) -> List[str]:
    file_models = database_manager.select('files', FileModel, Conditions(upload_id=upload_id), row_limit=100)
    return [await discord_client.fetch_attachment_url(file_model.message_id, CHANNEL_ID) for file_model in file_models]


@app.get("/upload/{upload_id}")
async def get_upload_files(upload_id: int) -> Dict[str, List[str]]:
    return {"urls": await get_upload_urls(upload_id)}


@app.get("/collection/{collection_id}")
async def get_collection_files(collection_id: int) -> Dict[int, List[str]]:
    upload_models = database_manager.select('uploads', UploadModel, Conditions(collection_id=collection_id),
                                            row_limit=100)
    return {upload_model.id: await get_upload_urls(upload_model.id) for upload_model in upload_models}


async def upload_file_parts(file: UploadFile, upload_id: int) -> None:
    async for part_path in split_file(file):
        message_id = await discord_client.upload_file(part_path, file.filename, CHANNEL_ID)
        delete_file(part_path)
        file_model = FileModel(message_id=message_id, upload_id=upload_id)
        database_manager.insert('files', file_model)


@app.post("/upload/")
async def create_upload_file(file: UploadFile) -> Dict[str, str]:
    logger.info(f"uploading {file.filename}")
    upload = UploadModel(user_id='1', size=file.size, upload_time=datetime.now())
    result = database_manager.insert('uploads', upload)
    upload_id = int(result.lastrowid)
    await upload_file_parts(file, upload_id)
    return {"upload_id": str(upload_id)}
