import os
import uuid

from fastapi import UploadFile
from typing import AsyncGenerator

CHUNK_SIZE = 1024 * 1024 * 5


async def read_file_chunks(upload_file: UploadFile) -> AsyncGenerator[bytes, None]:
    buffer = await upload_file.read(CHUNK_SIZE)
    while buffer:
        yield buffer
        buffer = await upload_file.read(CHUNK_SIZE)


async def split_file(upload_file: UploadFile) -> AsyncGenerator[str, None]:
    async for buffer in read_file_chunks(upload_file):
        part_path = f'{upload_file.filename}_{uuid.uuid4()}'
        with open(part_path, 'wb') as file_part:
            file_part.write(buffer)
        yield part_path


def delete_file(path: str) -> None:
    os.remove(path)
