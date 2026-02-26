"""Configuración — lee st.secrets en Streamlit Cloud, fallback a valores locales."""

import streamlit as st

def _s(key, fallback=""):
    try:
        return st.secrets[key]
    except Exception:
        return fallback

SUPABASE_URL = _s("SUPABASE_URL", "https://efomzdzxkwfmzbturvat.supabase.co")
SUPABASE_KEY = _s("SUPABASE_KEY", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImVmb216ZHp4a3dmbXpidHVydmF0Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3Njg3NDg1NDIsImV4cCI6MjA4NDMyNDU0Mn0.j0XDhxsBhZpcQ4sGjKLPvbmcMKHxalzfAp7qOdywYQQ")

# Escala de evaluación
ESCALA = {
    1: "Nunca",
    2: "Rara vez",
    3: "A veces",
    4: "Frecuentemente",
    5: "Siempre",
}
