"""CRUD de eventos (área admin)."""

from datetime import datetime

from flask import flash, redirect, render_template, request, url_for
from sqlalchemy import select

from auth import admin_required
from cache import invalidate_public_cache
from database import get_session
from models.evento import Evento
from routes.admin import bp
from validators import (
    MAX_TITLE as V_MAX_TITLE,
    clamp_str,
    validate_evento_nome,
    validate_evento_numbers,
)


def _disponivel_from_form() -> bool:
    return request.form.get("disponivel") == "1"


def _parse_data(s: str | None):
    if not s:
        return None
    try:
        return datetime.strptime(s.strip(), "%Y-%m-%d").date()
    except ValueError:
        return None


def _parse_horario(s: str | None):
    if not s:
        return None
    s = s.strip()
    for fmt in ("%H:%M", "%H:%M:%S"):
        try:
            return datetime.strptime(s, fmt).time()
        except ValueError:
            continue
    return None


@bp.route("/eventos")
@admin_required
def eventos_list():
    db = get_session()
    try:
        eventos = db.scalars(select(Evento).order_by(Evento.data.desc(), Evento.horario.desc())).all()
    finally:
        db.close()
    return render_template(
        "admin/eventos_list.html",
        active="admin",
        eventos=eventos,
    )


@bp.route("/eventos/novo", methods=["GET", "POST"])
@admin_required
def eventos_novo():
    if request.method == "POST":
        nome = request.form.get("nome")
        data_s = request.form.get("data") or ""
        horario_s = request.form.get("horario") or ""
        disp_s = (request.form.get("disponibilidade") or "").strip()
        disp_bool = _disponivel_from_form()

        err_nome, nome_ok = validate_evento_nome(nome)
        if err_nome:
            flash(err_nome, "error")
            return render_template(
                "admin/evento_form.html",
                active="admin",
                evento=None,
                form_nome=clamp_str(nome, V_MAX_TITLE),
                form_data=data_s,
                form_horario=horario_s,
                form_disponibilidade=disp_s,
                form_disponivel=disp_bool,
            )

        data = _parse_data(data_s)
        horario = _parse_horario(horario_s)
        try:
            disponibilidade = int(disp_s) if disp_s != "" else -1
        except ValueError:
            disponibilidade = -1

        err_vagas = validate_evento_numbers(disponibilidade)
        if err_vagas or data is None or horario is None:
            flash(
                err_vagas
                or "Preencha data e horário válidos e vagas numéricas.",
                "error",
            )
            return render_template(
                "admin/evento_form.html",
                active="admin",
                evento=None,
                form_nome=nome_ok or "",
                form_data=data_s,
                form_horario=horario_s,
                form_disponibilidade=disp_s,
                form_disponivel=disp_bool,
            )

        assert nome_ok is not None
        db = get_session()
        try:
            e = Evento(
                nome=nome_ok,
                data=data,
                horario=horario,
                disponibilidade=disponibilidade,
                disponivel=disp_bool,
            )
            db.add(e)
            db.commit()
            invalidate_public_cache()
            flash("Evento criado.", "info")
            return redirect(url_for("admin.eventos_list"))
        finally:
            db.close()

    return render_template(
        "admin/evento_form.html",
        active="admin",
        evento=None,
        form_nome="",
        form_data="",
        form_horario="",
        form_disponibilidade="0",
        form_disponivel=True,
    )


@bp.route("/eventos/<int:evento_id>/editar", methods=["GET", "POST"])
@admin_required
def eventos_editar(evento_id: int):
    db = get_session()
    try:
        evento = db.get(Evento, evento_id)
        if evento is None:
            flash("Evento não encontrado.", "error")
            return redirect(url_for("admin.eventos_list"))

        if request.method == "POST":
            nome = request.form.get("nome")
            data_s = request.form.get("data") or ""
            horario_s = request.form.get("horario") or ""
            disp_s = (request.form.get("disponibilidade") or "").strip()
            disp_bool = _disponivel_from_form()

            err_nome, nome_ok = validate_evento_nome(nome)
            if err_nome:
                flash(err_nome, "error")
                return render_template(
                    "admin/evento_form.html",
                    active="admin",
                    evento=evento,
                    form_nome=clamp_str(nome, V_MAX_TITLE),
                    form_data=data_s,
                    form_horario=horario_s,
                    form_disponibilidade=disp_s,
                    form_disponivel=disp_bool,
                )

            data = _parse_data(data_s)
            horario = _parse_horario(horario_s)
            try:
                disponibilidade = int(disp_s) if disp_s != "" else -1
            except ValueError:
                disponibilidade = -1

            err_vagas = validate_evento_numbers(disponibilidade)
            if err_vagas or data is None or horario is None:
                flash(
                    err_vagas
                    or "Preencha data e horário válidos e vagas numéricas.",
                    "error",
                )
                return render_template(
                    "admin/evento_form.html",
                    active="admin",
                    evento=evento,
                    form_nome=nome_ok or "",
                    form_data=data_s,
                    form_horario=horario_s,
                    form_disponibilidade=disp_s,
                    form_disponivel=disp_bool,
                )

            assert nome_ok is not None
            evento.nome = nome_ok
            evento.data = data
            evento.horario = horario
            evento.disponibilidade = disponibilidade
            evento.disponivel = disp_bool
            db.commit()
            invalidate_public_cache()
            flash("Evento atualizado.", "info")
            return redirect(url_for("admin.eventos_list"))
    finally:
        db.close()

    return render_template(
        "admin/evento_form.html",
        active="admin",
        evento=evento,
        form_nome=evento.nome,
        form_data=evento.data.isoformat(),
        form_horario=evento.horario.strftime("%H:%M"),
        form_disponibilidade=str(evento.disponibilidade),
        form_disponivel=evento.disponivel,
    )


@bp.route("/eventos/<int:evento_id>/excluir", methods=["POST"])
@admin_required
def eventos_excluir(evento_id: int):
    db = get_session()
    try:
        evento = db.get(Evento, evento_id)
        if evento is None:
            flash("Evento não encontrado.", "error")
            return redirect(url_for("admin.eventos_list"))
        db.delete(evento)
        db.commit()
        invalidate_public_cache()
        flash("Evento excluído.", "info")
    finally:
        db.close()
    return redirect(url_for("admin.eventos_list"))
