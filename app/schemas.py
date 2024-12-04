from pydantic import BaseModel
from datetime import datetime

class FileMetadataSchema(BaseModel):
    id: int
    filename: str
    size: int
    uploaded_at: datetime
    completed: bool

    class Config:
        orm_mode = True
