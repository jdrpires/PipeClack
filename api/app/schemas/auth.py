from pydantic import BaseModel, EmailStr
from typing import List

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    roles: List[str] = []

class UserRead(BaseModel):
    id: int
    name: str
    email: EmailStr
    roles: List[str]
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
