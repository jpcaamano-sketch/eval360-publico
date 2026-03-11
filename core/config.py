"""Configuración central de Evaluación 360 v2."""

import os

def _cfg(key, default=""):
    """Lee desde variables de entorno (Streamlit Secrets las inyecta como env vars),
    o cae al valor por defecto para desarrollo local."""
    return os.environ.get(key, default)


SUPABASE_URL = _cfg("SUPABASE_URL", "https://efomzdzxkwfmzbturvat.supabase.co")
SUPABASE_KEY = _cfg("SUPABASE_KEY", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImVmb216ZHp4a3dmbXpidHVydmF0Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3Njg3NDg1NDIsImV4cCI6MjA4NDMyNDU0Mn0.j0XDhxsBhZpcQ4sGjKLPvbmcMKHxalzfAp7qOdywYQQ")

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT   = 587
SMTP_USER   = _cfg("SMTP_USER",   "jpcaamano@gmail.com")
SMTP_PASSWORD = _cfg("SMTP_PASSWORD", "fgwd snko oebq vafx")

ADMIN_PASSWORD = _cfg("ADMIN_PASSWORD", "admin360")

GOOGLE_API_KEY = _cfg("GOOGLE_API_KEY", "AIzaSyBvCGMkdcgzaDgv9vPJ_MXT43c13UX0QQ0")

# URLs de las aplicaciones (Streamlit Cloud — URL permanente)
APP_AUTO_URL      = "https://eval360-yocreo.streamlit.app"
APP_FEEDBACK_URL  = "https://eval360-yocreo.streamlit.app"

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
