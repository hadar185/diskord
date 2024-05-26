from typing import Optional
from pydantic import BaseModel


class FileModel(BaseModel):
    id: Optional[int] = None
    message_id: int
    upload_id: int
