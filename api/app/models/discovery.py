from datetime import datetime
from sqlalchemy import Integer, ForeignKey, String, DateTime, JSON
from sqlalchemy.orm import Mapped, mapped_column
from . import Base

class DiscoveryTemplate(Base):
    __tablename__ = "discovery_templates"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    titulo: Mapped[str] = mapped_column(String(200))
    conteudo_json: Mapped[dict] = mapped_column(JSON)

class DiscoveryResponse(Base):
    __tablename__ = "discovery_responses"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id", ondelete="CASCADE"))
    template_id: Mapped[int] = mapped_column(ForeignKey("discovery_templates.id"))
    respostas_json: Mapped[dict] = mapped_column(JSON)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
