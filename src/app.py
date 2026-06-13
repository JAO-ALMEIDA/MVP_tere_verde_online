"""Aplicação principal Flask — tere_verde_online."""

from __future__ import annotations

import os

import click
from flask import Flask

from database import init_db


def create_app() -> Flask:
    app = Flask(
        __name__,
        template_folder="templates",
        static_folder="static",
    )
    secret = os.environ.get("SECRET_KEY", "dev-secret-change-me")
    app.config["SECRET_KEY"] = secret
    app.config["SESSION_COOKIE_HTTPONLY"] = True
    app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
    app.config["SESSION_COOKIE_SECURE"] = bool(
        int(os.environ.get("SESSION_COOKIE_SECURE", "0"))
    )

    init_db()

    from routes.admin import bp as admin_bp
    from routes.main import bp as main_bp

    app.register_blueprint(admin_bp)
    app.register_blueprint(main_bp)

    @app.context_processor
    def inject_admin_context():
        from auth import get_admin_id, get_admin_usuario

        return {
            "admin_logged_in": get_admin_id() is not None,
            "admin_usuario": get_admin_usuario() or "",
        }

    @app.cli.command("create-admin")
    @click.argument("usuario")
    @click.argument("senha")
    def create_admin_cli(usuario: str, senha: str) -> None:
        """Cria um administrador (senha armazenada com hash)."""
        from sqlalchemy import select

        from auth import hash_password
        from database import get_session
        from models.administrador import Administrador
        from validators import validate_new_admin_password

        err = validate_new_admin_password(senha)
        if err:
            click.echo(f"Erro: {err}", err=True)
            return

        init_db()
        db = get_session()
        try:
            exists = db.scalar(
                select(Administrador).where(Administrador.usuario == usuario.strip())
            )
            if exists:
                click.echo("Erro: usuário já existe.", err=True)
                return
            admin = Administrador(
                usuario=usuario.strip(),
                senha_hash=hash_password(senha),
            )
            db.add(admin)
            db.commit()
            click.echo("Administrador criado.")
        finally:
            db.close()

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)
