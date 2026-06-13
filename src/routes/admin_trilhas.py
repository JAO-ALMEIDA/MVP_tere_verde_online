"""CRUD de trilhas (área admin)."""

from flask import flash, redirect, render_template, request, url_for
from sqlalchemy import select

from auth import admin_required
from cache import invalidate_public_cache
from database import get_session
from models.trilha import Trilha
from routes.admin import bp
from validators import (
    MAX_DESC as V_MAX_DESC,
    MAX_TITLE as V_MAX_TITLE,
    clamp_str,
    validate_trilha_form,
)


def _disponivel_from_form() -> bool:
    return request.form.get("disponivel") == "1"


@bp.route("/trilhas")
@admin_required
def trilhas_list():
    db = get_session()
    try:
        trilhas = db.scalars(select(Trilha).order_by(Trilha.nome)).all()
    finally:
        db.close()
    return render_template(
        "admin/trilhas_list.html",
        active="admin",
        trilhas=trilhas,
    )


@bp.route("/trilhas/nova", methods=["GET", "POST"])
@admin_required
def trilhas_nova():
    if request.method == "POST":
        nome = request.form.get("nome")
        dificuldade = request.form.get("dificuldade")
        descricao = request.form.get("descricao")
        status = request.form.get("status")
        disp = _disponivel_from_form()
        err, data = validate_trilha_form(nome, dificuldade, descricao, status)
        if err:
            flash(err, "error")
            return render_template(
                "admin/trilha_form.html",
                active="admin",
                trilha=None,
                form_nome=clamp_str(nome, V_MAX_TITLE),
                form_dificuldade=(dificuldade or "facil").strip().lower() or "facil",
                form_descricao=clamp_str(descricao, V_MAX_DESC),
                form_status=(status or "ativa").strip().lower() or "ativa",
                form_disponivel=disp,
            )
        assert data is not None
        db = get_session()
        try:
            t = Trilha(
                nome=data["nome"],
                dificuldade=data["dificuldade"],
                descricao=data["descricao"],
                status=data["status"],
                disponivel=disp,
            )
            db.add(t)
            db.commit()
            invalidate_public_cache()
            flash("Trilha criada.", "info")
            return redirect(url_for("admin.trilhas_list"))
        finally:
            db.close()

    return render_template(
        "admin/trilha_form.html",
        active="admin",
        trilha=None,
        form_nome="",
        form_dificuldade="facil",
        form_descricao="",
        form_status="ativa",
        form_disponivel=True,
    )


@bp.route("/trilhas/<int:trilha_id>/editar", methods=["GET", "POST"])
@admin_required
def trilhas_editar(trilha_id: int):
    db = get_session()
    try:
        trilha = db.get(Trilha, trilha_id)
        if trilha is None:
            flash("Trilha não encontrada.", "error")
            return redirect(url_for("admin.trilhas_list"))

        if request.method == "POST":
            nome = request.form.get("nome")
            dificuldade = request.form.get("dificuldade")
            descricao = request.form.get("descricao")
            status = request.form.get("status")
            disp = _disponivel_from_form()
            err, data = validate_trilha_form(nome, dificuldade, descricao, status)
            if err:
                flash(err, "error")
                return render_template(
                    "admin/trilha_form.html",
                    active="admin",
                    trilha=trilha,
                    form_nome=clamp_str(nome, V_MAX_TITLE),
                    form_dificuldade=(dificuldade or "facil").strip().lower() or "facil",
                    form_descricao=clamp_str(descricao, V_MAX_DESC),
                    form_status=(status or "ativa").strip().lower() or "ativa",
                    form_disponivel=disp,
                )
            assert data is not None
            trilha.nome = data["nome"]
            trilha.dificuldade = data["dificuldade"]
            trilha.descricao = data["descricao"]
            trilha.status = data["status"]
            trilha.disponivel = disp
            db.commit()
            invalidate_public_cache()
            flash("Trilha atualizada.", "info")
            return redirect(url_for("admin.trilhas_list"))
    finally:
        db.close()

    return render_template(
        "admin/trilha_form.html",
        active="admin",
        trilha=trilha,
        form_nome=trilha.nome,
        form_dificuldade=trilha.dificuldade,
        form_descricao=trilha.descricao,
        form_status=trilha.status,
        form_disponivel=trilha.disponivel,
    )


@bp.route("/trilhas/<int:trilha_id>/excluir", methods=["POST"])
@admin_required
def trilhas_excluir(trilha_id: int):
    db = get_session()
    try:
        trilha = db.get(Trilha, trilha_id)
        if trilha is None:
            flash("Trilha não encontrada.", "error")
            return redirect(url_for("admin.trilhas_list"))
        db.delete(trilha)
        db.commit()
        invalidate_public_cache()
        flash("Trilha excluída.", "info")
    finally:
        db.close()
    return redirect(url_for("admin.trilhas_list"))
