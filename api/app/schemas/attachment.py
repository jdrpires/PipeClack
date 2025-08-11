from pydantic import BaseModel

class AttachmentRead(BaseModel):
    id: int
    filename: str
    path: str
    class Config:
        from_attributes = True
