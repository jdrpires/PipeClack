from sqlalchemy import Integer, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from . import Base

class Column(Base):
    __tablename__ = "columns"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    board_id: Mapped[int] = mapped_column(ForeignKey("boards.id", ondelete="CASCADE"))
    nome: Mapped[str] = mapped_column(String(100))
    ordem: Mapped[int] = mapped_column(Integer)
    board = relationship("Board", back_populates="columns")
    cards = relationship("Card", back_populates="column")
