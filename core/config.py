"""Configuración central de Evaluación 360 v2."""

import os

def _cfg(key, default=""):
    """Lee desde variables de entorno (Streamlit Secrets las inyecta como env vars),
    o cae al valor por defecto para desarrollo local."""
    return os.environ.get(key, default)


SUPABASE_URL = _cfg("SUPABASE_URL")
SUPABASE_KEY = _cfg("SUPABASE_KEY")

RESEND_API_KEY = _cfg("RESEND_API_KEY")
FROM_EMAIL     = "Evaluación 360 <noreply@escuelayocreo.cl>"

ADMIN_PASSWORD = _cfg("ADMIN_PASSWORD")

GOOGLE_API_KEY = _cfg("GOOGLE_API_KEY", "")

# URLs de las aplicaciones (configuradas como variables de entorno en Railway)
APP_AUTO_URL     = _cfg("APP_AUTO_URL",     "http://localhost:8507")
APP_FEEDBACK_URL = _cfg("APP_FEEDBACK_URL", "http://localhost:8508")
APP_CC_URL       = _cfg("APP_CC_URL",       "http://localhost:8509")

# Escala de evaluación
ESCALA = {
    1: "Nunca",
    2: "Rara vez",
    3: "A veces",
    4: "Frecuentemente",
    5: "Siempre",
}

# Constantes de negocio
MIN_EVALUADORES  = 3
MAX_EVALUADORES  = 5
UMBRAL_MEJORAR   = 3.5
