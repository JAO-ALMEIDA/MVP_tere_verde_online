"""CRUD de biodiversidade (área admin)."""

from flask import flash, redirect, render_template, request, url_for
from sqlalchemy import select

from auth import admin_required
from cache import invalidate_public_cache
from database import get_session
from models.biodiversidade import Biodiversidade
from routes.admin import bp
from validators import (
    MAX_DESC as V_MAX_DESC,
    MAX_TIPO as V_MAX_TIPO,
    MAX_TITLE as V_MAX_TITLE,
    clamp_str,
    validate_biodiversidade_form,
)


@bp.route("/biodiversidade")
@admin_required
def biodiversidade_list():
    db = get_session()
    try:
        itens = db.scalars(select(Biodiversidade).order_by(Biodiversidade.nome)).all()
    finally:
        db.close()
    return render_template(
        "admin/biodiversidade_list.html",
        active="admin",
        itens=itens,
    )


@bp.route("/biodiversidade/nova", methods=["GET", "POST"])
@admin_required
def biodiversidade_nova():
    if request.method == "POST":
        nome = request.form.get("nome")
        tipo = request.form.get("tipo")
        descricao = request.form.get("descricao")
        err, data = validate_biodiversidade_form(nome, tipo, descricao)
        if err:
            flash(err, "error")
            return render_template(
                "admin/biodiversidade_form.html",
                active="admin",
                item=None,
                form_nome=clamp_str(nome, V_MAX_TITLE),
                form_tipo=clamp_str(tipo, V_MAX_TIPO),
                form_descricao=clamp_str(descricao, V_MAX_DESC),
            )
        assert data is not None
        db = get_session()
        try:
            b = Biodiversidade(
                nome=data["nome"],
                tipo=data["tipo"],
                descricao=data["descricao"],
            )
            db.add(b)
            db.commit()
            invalidate_public_cache()
            flash("Registro criado.", "info")
            return redirect(url_for("admin.biodiversidade_list"))
        finally:
            db.close()

    return render_template(
        "admin/biodiversidade_form.html",
        active="admin",
        item=None,
        form_nome="",
        form_tipo="",
        form_descricao="",
    )


@bp.route("/biodiversidade/<int:item_id>/editar", methods=["GET", "POST"])
@admin_required
def biodiversidade_editar(item_id: int):
    db = get_session()
    try:
        item = db.get(Biodiversidade, item_id)
        if item is None:
            flash("Registro não encontrado.", "error")
            return redirect(url_for("admin.biodiversidade_list"))

        if request.method == "POST":
            nome = request.form.get("nome")
            tipo = request.form.get("tipo")
            descricao = request.form.get("descricao")
            err, data = validate_biodiversidade_form(nome, tipo, descricao)
            if err:
                flash(err, "error")
                return render_template(
                    "admin/biodiversidade_form.html",
                    active="admin",
                    item=item,
                    form_nome=clamp_str(nome, V_MAX_TITLE),
                    form_tipo=clamp_str(tipo, V_MAX_TIPO),
                    form_descricao=clamp_str(descricao, V_MAX_DESC),
                )
            assert data is not None
            item.nome = data["nome"]
            item.tipo = data["tipo"]
            item.descricao = data["descricao"]
            db.commit()
            invalidate_public_cache()
            flash("Registro atualizado.", "info")
            return redirect(url_for("admin.biodiversidade_list"))
    finally:
        db.close()

    return render_template(
        "admin/biodiversidade_form.html",
        active="admin",
        item=item,
        form_nome=item.nome,
        form_tipo=item.tipo,
        form_descricao=item.descricao,
    )


@bp.route("/biodiversidade/<int:item_id>/excluir", methods=["POST"])
@admin_required
def biodiversidade_excluir(item_id: int):
    db = get_session()
    try:
        item = db.get(Biodiversidade, item_id)
        if item is None:
            flash("Registro não encontrado.", "error")
            return redirect(url_for("admin.biodiversidade_list"))
        db.delete(item)
        db.commit()
        invalidate_public_cache()
        flash("Registro excluído.", "info")
    finally:
        db.close()
    return redirect(url_for("admin.biodiversidade_list"))
