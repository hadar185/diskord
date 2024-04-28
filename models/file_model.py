from pydantic import BaseModel


class FileModel(BaseModel):
    url: str
    upload_id: int
