"""Conexión a Supabase."""

from __future__ import annotations
import time
from typing import Optional
from supabase import create_client, Client
from core.config import SUPABASE_URL, SUPABASE_KEY

_client: Optional[Client] = None


def get_client() -> Client:
    """Retorna un cliente Supabase (singleton)."""
    global _client
    if _client is None:
        _client = create_client(SUPABASE_URL, SUPABASE_KEY)
    return _client


def reset_client():
    """Fuerza recrear el cliente (útil tras errores SSL)."""
    global _client
    _client = None


def ejecutar_con_reintento(fn, max_intentos=3):
    """Ejecuta una función con reintentos ante errores de conexión."""
    for intento in range(max_intentos):
        try:
            return fn()
        except Exception as e:
            err_str = str(e).lower()
            if "ssl" in err_str or "eof" in err_str or "disconnect" in err_str or "remote" in err_str:
                reset_client()
                if intento < max_intentos - 1:
                    time.sleep(1)
                    continue
            raise
