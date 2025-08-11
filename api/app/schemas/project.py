from pydantic import BaseModel
from typing import Optional
from ..models.project import ProjectStatus

class ProjectCreate(BaseModel):
    name: str
    status: ProjectStatus | None = None

class ProjectRead(BaseModel):
    id: int
    name: str
    status: ProjectStatus
    class Config:
        from_attributes = True
