from typing import Optional
from pydantic import BaseModel


class FileModel(BaseModel):
    id: Optional[int] = None
    url: str
    upload_id: int
