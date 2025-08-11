from pydantic import BaseModel
from ..models.board import BoardType

class BoardCreate(BaseModel):
    tipo: BoardType

class BoardRead(BaseModel):
    id: int
    project_id: int
    tipo: BoardType
    class Config:
        from_attributes = True
