from datetime import datetime
from sqlalchemy import Integer, ForeignKey, String, Enum, Float, Text, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from enum import Enum as PyEnum
from . import Base

class CardPriority(str, PyEnum):
    BAIXA = "BAIXA"
    MEDIA = "MEDIA"
    ALTA = "ALTA"
    CRITICA = "CRITICA"

class Card(Base):
    __tablename__ = "cards"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    board_id: Mapped[int] = mapped_column(ForeignKey("boards.id", ondelete="CASCADE"))
    column_id: Mapped[int] = mapped_column(ForeignKey("columns.id", ondelete="CASCADE"))
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id", ondelete="CASCADE"))
    titulo: Mapped[str] = mapped_column(String(200))
    descricao: Mapped[str] = mapped_column(Text, default="")
    prioridade: Mapped[CardPriority] = mapped_column(Enum(CardPriority), default=CardPriority.MEDIA)
    position: Mapped[float] = mapped_column(Float, default=1000.0)
    created_by: Mapped[int] = mapped_column(ForeignKey("users.id"))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    column = relationship("Column", back_populates="cards")
