from sqlalchemy import Integer, ForeignKey, Enum, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from enum import Enum as PyEnum
from . import Base

class BoardType(str, PyEnum):
    COMERCIAL = "COMERCIAL"
    PO = "PO"
    DEV = "DEV"

class Board(Base):
    __tablename__ = "boards"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id", ondelete="CASCADE"))
    tipo: Mapped[BoardType] = mapped_column(Enum(BoardType))
    ativo: Mapped[bool] = mapped_column(Boolean, default=True)
    columns = relationship("Column", cascade="all, delete", back_populates="board")
