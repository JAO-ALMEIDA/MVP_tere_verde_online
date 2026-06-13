"""Rotas da área administrativa."""

from flask import Blueprint, flash, redirect, render_template, request, url_for

from auth import (
    admin_required,
    authenticate,
    get_admin_id,
    get_admin_usuario,
    login_admin_user,
    logout_admin_user,
)
from validators import validate_admin_login

bp = Blueprint("admin", __name__, url_prefix="/admin")


def _safe_next_url(next_path: str | None) -> str | None:
    """Aceita apenas caminhos relativos na mesma aplicação."""
    if not next_path or not next_path.startswith("/"):
        return None
    if next_path.startswith("//"):
        return None
    return next_path


@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        if get_admin_id() is not None:
            return redirect(url_for("admin.dashboard"))
        next_hint = _safe_next_url(request.args.get("next"))
        return render_template(
            "login_admin.html",
            active="admin",
            next_url=next_hint or "",
        )

    usuario = (request.form.get("username") or "").strip()
    senha = request.form.get("password") or ""
    next_raw = request.form.get("next") or ""
    next_url = _safe_next_url(next_raw)

    login_err = validate_admin_login(usuario, senha)
    if login_err:
        flash(login_err, "error")
        return render_template(
            "login_admin.html",
            active="admin",
            next_url=next_raw,
        )

    admin = authenticate(usuario, senha)
    if admin is None:
        flash("Usuário ou senha incorretos.", "error")
        return render_template(
            "login_admin.html",
            active="admin",
            next_url=next_raw,
        )

    login_admin_user(admin)
    if next_url:
        return redirect(next_url)
    return redirect(url_for("admin.dashboard"))


@bp.route("")
@admin_required
def dashboard():
    return render_template(
        "admin/dashboard.html",
        active="admin",
        admin_usuario=get_admin_usuario() or "",
    )


@bp.route("/logout", methods=["POST"])
def logout():
    """Encerra a sessão (sempre permitido, mesmo sem sessão ativa)."""
    logout_admin_user()
    flash("Sessão encerrada.", "info")
    return redirect(url_for("admin.login"))


# Rotas CRUD (trilhas, eventos, biodiversidade)
from routes import admin_biodiversidade  # noqa: E402, F401
from routes import admin_eventos  # noqa: E402, F401
from routes import admin_trilhas  # noqa: E402, F401
