"""Configuración central de Evaluación 360 v2."""

import os

def _cfg(key, default=""):
    """Lee desde variables de entorno (Streamlit Secrets las inyecta como env vars),
    o cae al valor por defecto para desarrollo local."""
    return os.environ.get(key, default)


SUPABASE_URL = _cfg("SUPABASE_URL")
SUPABASE_KEY = _cfg("SUPABASE_KEY")

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT   = 587
SMTP_USER   = _cfg("SMTP_USER",   "jpcaamano@gmail.com")
SMTP_PASSWORD = _cfg("SMTP_PASSWORD")

ADMIN_PASSWORD = _cfg("ADMIN_PASSWORD")

GOOGLE_API_KEY = _cfg("GOOGLE_API_KEY", "")

# URLs de las aplicaciones (Streamlit Cloud — URL permanente)
APP_AUTO_URL      = "https://eval360-yocreo.streamlit.app"
APP_FEEDBACK_URL  = "https://eval360-yocreo.streamlit.app"
APP_CC_URL        = _cfg("APP_CC_URL", "https://eval360-cc.streamlit.app")

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
