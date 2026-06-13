"""Validação simples de entradas (sem dependências extras)."""

from __future__ import annotations

# Limites alinhados aos modelos / proteção contra payloads grandes
MAX_USERNAME = 128
MAX_PASSWORD_INPUT = 1024
MIN_PASSWORD_ADMIN = 8
MAX_TITLE = 255
MAX_TIPO = 128
MAX_DESC = 50000
MAX_DISPONIBILIDADE = 10_000_000

_ALLOWED_DIFFICULTY = frozenset({"facil", "moderado", "dificil"})
_ALLOWED_STATUS = frozenset({"ativa", "inativa", "manutencao"})


def clamp_str(s: str | None, max_len: int) -> str:
    """Remove espaços nas pontas e limita o tamanho."""
    v = (s or "").strip()
    if len(v) > max_len:
        return v[:max_len]
    return v


def validate_admin_login(username: str | None, password: str | None) -> str | None:
    """Devolve mensagem de erro ou ``None`` se o formato é aceitável."""
    u = (username or "").strip()
    p = password or ""
    if not u or not p:
        return "Informe usuário e senha."
    if len(u) > MAX_USERNAME or len(p) > MAX_PASSWORD_INPUT:
        return "Dados inválidos."
    return None


def validate_new_admin_password(senha: str) -> str | None:
    """CLI create-admin: senha com tamanho mínimo."""
    if len(senha) < MIN_PASSWORD_ADMIN:
        return f"A senha deve ter pelo menos {MIN_PASSWORD_ADMIN} caracteres."
    if len(senha) > MAX_PASSWORD_INPUT:
        return "Senha longa demais."
    return None


def validate_trilha_form(
    nome: str | None,
    dificuldade: str | None,
    descricao: str | None,
    status: str | None,
) -> tuple[str | None, dict | None]:
    """Devolve (erro, None) ou (None, campos validados)."""
    nome_c = clamp_str(nome, MAX_TITLE)
    desc_c = clamp_str(descricao, MAX_DESC)
    if not nome_c:
        return "Nome é obrigatório.", None
    if not desc_c:
        return "Descrição é obrigatória.", None
    dif = (dificuldade or "facil").strip().lower()
    if dif not in _ALLOWED_DIFFICULTY:
        dif = "facil"
    st = (status or "ativa").strip().lower()
    if st not in _ALLOWED_STATUS:
        st = "ativa"
    return None, {
        "nome": nome_c,
        "dificuldade": dif,
        "descricao": desc_c,
        "status": st,
    }


def validate_biodiversidade_form(
    nome: str | None,
    tipo: str | None,
    descricao: str | None,
) -> tuple[str | None, dict | None]:
    nome_c = clamp_str(nome, MAX_TITLE)
    tipo_c = clamp_str(tipo, MAX_TIPO)
    desc_c = clamp_str(descricao, MAX_DESC)
    if not nome_c or not tipo_c or not desc_c:
        return "Preencha nome, tipo e descrição.", None
    return None, {
        "nome": nome_c,
        "tipo": tipo_c,
        "descricao": desc_c,
    }


def validate_evento_numbers(disponibilidade: int) -> str | None:
    if disponibilidade < 0 or disponibilidade > MAX_DISPONIBILIDADE:
        return "Número de vagas inválido."
    return None


def validate_evento_nome(nome: str | None) -> tuple[str | None, str | None]:
    """Devolve (erro, nome_limpo)."""
    n = clamp_str(nome, MAX_TITLE)
    if not n:
        return "Informe o nome do evento.", None
    return None, n
