"""Autenticação de administrador (sessão + hash de senha)."""

from __future__ import annotations

from functools import wraps

from flask import redirect, request, session, url_for
from sqlalchemy import select
from werkzeug.security import check_password_hash, generate_password_hash

from database import get_session
from models.administrador import Administrador
from validators import MAX_PASSWORD_INPUT

SESSION_ADMIN_ID = "admin_id"
SESSION_ADMIN_USER = "admin_usuario"

# Hash fixo (senha fictícia) para manter custo semelhante quando o usuário não existe (mitigação de timing).
_DUMMY_PASSWORD_HASH = (
    "pbkdf2:sha256:1000000$bUkgw9gyCV1qfOhB$"
    "27f1488e83945243b2df6cf91f36d94bb6e8467166b3dbb6502d5c1c69881ab2"
)


def hash_password(plain: str) -> str:
    """Gera hash com algoritmo forte (scrypt se disponível no Werkzeug, senão pbkdf2)."""
    if len(plain) > MAX_PASSWORD_INPUT:
        raise ValueError("Senha longa demais.")
    try:
        return generate_password_hash(plain, method="scrypt:32768:8:1")
    except (ValueError, AttributeError, OSError):
        return generate_password_hash(plain, method="pbkdf2:sha256", salt_length=16)


def verify_password(plain: str, password_hash: str) -> bool:
    if len(plain) > MAX_PASSWORD_INPUT:
        return False
    return check_password_hash(password_hash, plain)


def authenticate(usuario: str, senha: str) -> Administrador | None:
    """Valida credenciais e devolve o registro ou ``None``."""
    db = get_session()
    try:
        stmt = select(Administrador).where(Administrador.usuario == usuario.strip())
        admin = db.scalar(stmt)
        if admin is None:
            check_password_hash(_DUMMY_PASSWORD_HASH, senha)
            return None
        if not verify_password(senha, admin.senha_hash):
            return None
        return admin
    finally:
        db.close()


def login_admin_user(admin: Administrador) -> None:
    session.clear()
    session[SESSION_ADMIN_ID] = admin.id
    session[SESSION_ADMIN_USER] = admin.usuario


def logout_admin_user() -> None:
    session.pop(SESSION_ADMIN_ID, None)
    session.pop(SESSION_ADMIN_USER, None)


def get_admin_id() -> int | None:
    raw = session.get(SESSION_ADMIN_ID)
    if raw is None:
        return None
    try:
        i = int(raw)
    except (TypeError, ValueError):
        session.clear()
        return None
    if i < 1:
        session.clear()
        return None
    return i


def get_admin_usuario() -> str | None:
    return session.get(SESSION_ADMIN_USER)


def admin_required(view):
    """Redireciona para o login se não houver sessão de administrador válida."""

    @wraps(view)
    def wrapped(*args, **kwargs):
        if get_admin_id() is None:
            return redirect(url_for("admin.login", next=request.path))
        return view(*args, **kwargs)

    return wrapped
