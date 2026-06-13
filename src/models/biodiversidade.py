"""Modelo Biodiversidade."""

from sqlalchemy import Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class Biodiversidade(Base):
    __tablename__ = "biodiversidades"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nome: Mapped[str] = mapped_column(String(255), nullable=False)
    tipo: Mapped[str] = mapped_column(String(128), nullable=False)
    descricao: Mapped[str] = mapped_column(Text, nullable=False)
