"""Configuração do banco SQLite e inicialização das tabelas."""

from __future__ import annotations

from pathlib import Path

from sqlalchemy import create_engine, event, inspect, text
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker


class Base(DeclarativeBase):
    """Base declarativa para os modelos SQLAlchemy."""


def _project_root() -> Path:
    return Path(__file__).resolve().parent.parent


def get_database_path() -> Path:
    """Caminho absoluto do arquivo SQLite em ``data/app.db``."""
    return _project_root() / "data" / "app.db"


def get_database_url() -> str:
    """URL de conexão SQLAlchemy para SQLite."""
    db_path = get_database_path()
    return f"sqlite:///{db_path.as_posix()}"


def get_engine(echo: bool = False):
    """Motor SQLAlchemy (SQLite) com timeouts para vários clientes concorrentes."""
    return create_engine(
        get_database_url(),
        echo=echo,
        pool_pre_ping=True,
        connect_args={
            "check_same_thread": False,
            "timeout": 30.0,
        },
    )


engine = get_engine()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@event.listens_for(engine, "connect")
def _sqlite_pragma(dbapi_conn, _connection_record) -> None:
    """WAL + busy timeout: leituras em paralelo; escritas menos bloqueantes."""
    cur = dbapi_conn.cursor()
    try:
        cur.execute("PRAGMA journal_mode=WAL")
        cur.execute("PRAGMA synchronous=NORMAL")
        cur.execute("PRAGMA busy_timeout=5000")
        cur.execute("PRAGMA foreign_keys=ON")
    finally:
        cur.close()


def init_db() -> None:
    """
    Garante a pasta ``data/``, importa os modelos e cria todas as tabelas.

    Deve ser chamada na instalação ou na primeira subida da aplicação.
    """
    data_dir = get_database_path().parent
    data_dir.mkdir(parents=True, exist_ok=True)

    # Registra metadados dos modelos antes de create_all
    from models.administrador import Administrador  # noqa: F401
    from models.biodiversidade import Biodiversidade  # noqa: F401
    from models.evento import Evento  # noqa: F401
    from models.trilha import Trilha  # noqa: F401

    Base.metadata.create_all(bind=engine)
    _migrate_disponivel_columns(engine)
    _ensure_indexes(engine)


# DDL literal por tabela (sem concatenação com dados externos — evita injeção em migrações).
_ALTER_DISPONIVEL_SQL = {
    "trilhas": (
        "ALTER TABLE trilhas ADD COLUMN disponivel INTEGER NOT NULL DEFAULT 1"
    ),
    "eventos": (
        "ALTER TABLE eventos ADD COLUMN disponivel INTEGER NOT NULL DEFAULT 1"
    ),
}


def _migrate_disponivel_columns(engine) -> None:
    """Adiciona coluna ``disponivel`` em bancos criados antes dessa versão."""
    insp = inspect(engine)
    for table in ("trilhas", "eventos"):
        try:
            cols = {c["name"] for c in insp.get_columns(table)}
        except Exception:
            continue
        if "disponivel" not in cols:
            ddl = _ALTER_DISPONIVEL_SQL.get(table)
            if not ddl:
                continue
            with engine.begin() as conn:
                conn.execute(text(ddl))


# Índices para ORDER BY / filtros frequentes (IF NOT EXISTS = seguro em upgrades).
_INDEX_DDL = (
    "CREATE INDEX IF NOT EXISTS ix_trilhas_nome ON trilhas (nome)",
    "CREATE INDEX IF NOT EXISTS ix_biodiversidades_nome ON biodiversidades (nome)",
    "CREATE INDEX IF NOT EXISTS ix_eventos_data_horario ON eventos (data, horario)",
)


def _ensure_indexes(engine) -> None:
    with engine.begin() as conn:
        for ddl in _INDEX_DDL:
            conn.execute(text(ddl))


def get_session() -> Session:
    """Abre uma sessão nova (fechar com ``session.close()``)."""
    return SessionLocal()
