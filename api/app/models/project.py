from datetime import datetime
from sqlalchemy import Integer, String, DateTime, Enum
from sqlalchemy.orm import Mapped, mapped_column
from enum import Enum as PyEnum
from . import Base

class ProjectStatus(str, PyEnum):
    EM_DISCOVERY = "EM_DISCOVERY"
    EM_PO = "EM_PO"
    EM_DEV = "EM_DEV"
    PAUSADO = "PAUSADO"
    CONCLUIDO = "CONCLUIDO"

class Project(Base):
    __tablename__ = "projects"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(200))
    status: Mapped[ProjectStatus] = mapped_column(Enum(ProjectStatus), default=ProjectStatus.EM_DISCOVERY)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
