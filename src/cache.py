"""Cache em memória simples (TTL) para páginas públicas — thread-safe."""

from __future__ import annotations

import threading
import time
from collections.abc import Callable
from typing import TypeVar

T = TypeVar("T")

# TTL curto: equilíbrio entre carga no SQLite com muitos leitores e dados atualizados após edição admin.
_DEFAULT_TTL = 45.0


class TTLCache:
    def __init__(self, ttl_seconds: float = _DEFAULT_TTL) -> None:
        self._ttl = ttl_seconds
        self._data: dict[str, tuple[float, object]] = {}
        self._lock = threading.Lock()

    def get_or_set(self, key: str, factory: Callable[[], T]) -> T:
        now = time.monotonic()
        with self._lock:
            item = self._data.get(key)
            if item is not None and item[0] > now:
                return item[1]  # type: ignore[return-value]
        val = factory()
        with self._lock:
            self._data[key] = (time.monotonic() + self._ttl, val)
            return val

    def invalidate(self) -> None:
        with self._lock:
            self._data.clear()


public_cache = TTLCache(ttl_seconds=_DEFAULT_TTL)


def invalidate_public_cache() -> None:
    """Chamar após qualquer alteração em trilhas, eventos ou biodiversidade (admin)."""
    public_cache.invalidate()
