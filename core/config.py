"""Configuración Evaluación 360 — formulario público."""

import streamlit as st

def _s(key, default=""):
    try:
        return st.secrets[key]
    except Exception:
        return default

SUPABASE_URL = "https://efomzdzxkwfmzbturvat.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImVmb216ZHp4a3dmbXpidHVydmF0Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3Njg3NDg1NDIsImV4cCI6MjA4NDMyNDU0Mn0.j0XDhxsBhZpcQ4sGjKLPvbmcMKHxalzfAp7qOdywYQQ"

SMTP_SERVER   = "smtp.gmail.com"
SMTP_PORT     = 587
SMTP_USER     = _s("SMTP_USER", "jpcaamano@gmail.com")
SMTP_PASSWORD = _s("SMTP_PASSWORD", "")

GOOGLE_API_KEY = _s("GOOGLE_API_KEY", "")

APP_AUTO_URL     = _s("APP_AUTO_URL", "https://eval360-yocreo.streamlit.app")
APP_FEEDBACK_URL = _s("APP_FEEDBACK_URL", "https://eval360-yocreo.streamlit.app")

ESCALA = {
    1: "Nunca",
    2: "Rara vez",
    3: "A veces",
    4: "Frecuentemente",
    5: "Siempre",
}
