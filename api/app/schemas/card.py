from pydantic import BaseModel
from ..models.card import CardPriority

class CardCreate(BaseModel):
    column_id: int
    titulo: str
    descricao: str = ""
    prioridade: CardPriority = CardPriority.MEDIA

class CardRead(BaseModel):
    id: int
    board_id: int
    column_id: int
    titulo: str
    prioridade: CardPriority
    position: float
    class Config:
        from_attributes = True

class CardMove(BaseModel):
    to_column_id: int
    position: float
