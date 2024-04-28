from typing import Optional
from datetime import datetime
from pydantic import BaseModel


class UploadModel(BaseModel):
    id: Optional[int] = None
    user_id: int
    album_id: Optional[int] = None
    size: int
    upload_time: datetime
