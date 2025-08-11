from pydantic import BaseModel

class CommentCreate(BaseModel):
    texto: str

class CommentRead(BaseModel):
    id: int
    card_id: int
    author_user_id: int
    texto: str
    class Config:
        from_attributes = True
