"""Consultas otimizadas para páginas públicas (apenas colunas usadas no HTML)."""

from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import load_only

from database import get_session
from models.biodiversidade import Biodiversidade
from models.evento import Evento
from models.trilha import Trilha


def fetch_trilhas_public():
    db = get_session()
    try:
        stmt = (
            select(Trilha)
            .order_by(Trilha.nome)
            .options(
                load_only(
                    Trilha.id,
                    Trilha.nome,
                    Trilha.dificuldade,
                    Trilha.descricao,
                    Trilha.status,
                    Trilha.disponivel,
                )
            )
        )
        return db.scalars(stmt).all()
    finally:
        db.close()


def fetch_biodiversidade_public():
    db = get_session()
    try:
        stmt = (
            select(Biodiversidade)
            .order_by(Biodiversidade.nome)
            .options(
                load_only(
                    Biodiversidade.id,
                    Biodiversidade.nome,
                    Biodiversidade.tipo,
                    Biodiversidade.descricao,
                )
            )
        )
        return db.scalars(stmt).all()
    finally:
        db.close()


def fetch_eventos_public():
    db = get_session()
    try:
        stmt = (
            select(Evento)
            .order_by(Evento.data, Evento.horario)
            .options(
                load_only(
                    Evento.id,
                    Evento.nome,
                    Evento.data,
                    Evento.horario,
                    Evento.disponibilidade,
                    Evento.disponivel,
                )
            )
        )
        return db.scalars(stmt).all()
    finally:
        db.close()
