from pydantic import BaseModel
from typing import Any

class DiscoveryTemplateRead(BaseModel):
    id: int
    titulo: str
    conteudo_json: dict
    class Config:
        from_attributes = True

class DiscoveryResponseCreate(BaseModel):
    template_id: int
    respostas_json: dict
