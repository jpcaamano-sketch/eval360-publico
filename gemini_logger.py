"""
gemini_logger.py — Módulo compartido para registrar uso de la API Gemini.

Uso en cualquier app:
    from gemini_logger import log_gemini

    response = model.generate_content(prompt)
    log_gemini("MiApp", "gemini-2.5-flash", response, "Descripción opcional")
"""

import os
import json
import urllib.request

SUPABASE_URL = os.environ.get("SUPABASE_URL", "")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY", "")

# Precios USD por 1M tokens (actualizar si cambian)
PRECIOS = {
    "gemini-2.5-flash":  {"entrada": 0.15,  "salida": 0.60},
    "gemini-2.0-flash":  {"entrada": 0.10,  "salida": 0.40},
    "gemini-1.5-flash":  {"entrada": 0.075, "salida": 0.30},
    "gemini-1.5-pro":    {"entrada": 1.25,  "salida": 5.00},
    "gemini-1.0-pro":    {"entrada": 0.50,  "salida": 1.50},
}

def log_gemini(app_nombre: str, modelo: str, response, descripcion: str = ""):
    """
    Registra una llamada a Gemini en Supabase.

    Parámetros:
        app_nombre  : Nombre de la app que hizo la llamada (ej. "Evaluacion360")
        modelo      : Nombre del modelo (ej. "gemini-2.5-flash")
        response    : El objeto response de model.generate_content()
        descripcion : Texto opcional describiendo para qué fue la llamada
    """
    try:
        meta = getattr(response, "usage_metadata", None)
        tokens_entrada = getattr(meta, "prompt_token_count", 0) or 0
        tokens_salida  = getattr(meta, "candidates_token_count", 0) or 0

        precio = PRECIOS.get(modelo, {"entrada": 0.15, "salida": 0.60})
        costo  = (tokens_entrada * precio["entrada"] + tokens_salida * precio["salida"]) / 1_000_000

        payload = json.dumps({
            "app_nombre":     app_nombre,
            "modelo":         modelo,
            "tokens_entrada": tokens_entrada,
            "tokens_salida":  tokens_salida,
            "costo_usd":      round(costo, 8),
            "descripcion":    descripcion or None,
        }).encode("utf-8")

        req = urllib.request.Request(
            f"{SUPABASE_URL}/rest/v1/gemini_uso",
            data=payload,
            method="POST",
            headers={
                "Content-Type": "application/json",
                "apikey": SUPABASE_KEY,
                "Authorization": f"Bearer {SUPABASE_KEY}",
                "Prefer": "return=minimal",
            },
        )
        urllib.request.urlopen(req, timeout=5)
    except Exception:
        pass  # El tracker nunca debe romper la app principal
