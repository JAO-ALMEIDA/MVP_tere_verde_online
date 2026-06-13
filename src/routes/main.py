"""Rotas principais."""

from flask import Blueprint, render_template

from cache import public_cache
from public_queries import (
    fetch_biodiversidade_public,
    fetch_eventos_public,
    fetch_trilhas_public,
)

bp = Blueprint("main", __name__)


@bp.route("/")
def home():
    return render_template("home.html", active="home")


@bp.route("/trilhas")
def trilhas():
    rows = public_cache.get_or_set("public_trilhas", fetch_trilhas_public)
    return render_template("trilhas.html", active="trilhas", trilhas=rows)


@bp.route("/biodiversidade")
def biodiversidade():
    rows = public_cache.get_or_set("public_bio", fetch_biodiversidade_public)
    return render_template("biodiversidade.html", active="biodiversidade", itens=rows)


@bp.route("/eventos")
def eventos():
    rows = public_cache.get_or_set("public_eventos", fetch_eventos_public)
    return render_template("eventos.html", active="eventos", eventos=rows)
