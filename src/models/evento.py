"""Modelo Evento."""

from datetime import date, time

from sqlalchemy import Boolean, Date, Integer, String, Time, true
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class Evento(Base):
    __tablename__ = "eventos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nome: Mapped[str] = mapped_column(String(255), nullable=False)
    data: Mapped[date] = mapped_column(Date, nullable=False)
    horario: Mapped[time] = mapped_column(Time, nullable=False)
    disponibilidade: Mapped[int] = mapped_column(Integer, nullable=False)
    disponivel: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        server_default=true(),
    )
