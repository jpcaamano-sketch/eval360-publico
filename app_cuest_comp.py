"""
Cuestionario Complementario — Formulario público
Acceso por token de evaluador.
"""

import streamlit as st
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from core import queries

st.set_page_config(
    page_title="Cuestionario Complementario",
    page_icon="💬",
    layout="centered",
)

st.markdown("""
<style>
    #MainMenu { visibility: hidden; }
    footer    { visibility: hidden; }
    textarea  { font-size: 1rem !important; }
</style>
""", unsafe_allow_html=True)

# ============================================================
# TOKEN
# ============================================================

token = st.query_params.get("token")

if not token:
    st.warning("Acceso no válido. Utiliza el enlace que recibiste por email.")
    st.stop()

evaluador = queries.cc_obtener_evaluador_por_token(token)

if not evaluador:
    st.error("Token no válido o expirado.")
    st.stop()

if evaluador.get("completado"):
    st.success(f"¡Gracias, {evaluador['nombre']}! Ya enviaste tus respuestas.")
    st.balloons()
    st.stop()

evaluado = evaluador.get("cc_evaluados") or {}
evaluado_nombre = evaluado.get("nombre", "el evaluado")
evaluado_area   = evaluado.get("area") or "su área"

# ============================================================
# FORMULARIO
# ============================================================

st.title("Cuestionario Complementario")
st.markdown(
    f"**Hola, {evaluador['nombre']}** — Estás respondiendo sobre **{evaluado_nombre}**. "
    "Tus respuestas son **anónimas**."
)
st.divider()

with st.form("form_cc"):
    st.markdown("### 🟢 Continuar haciendo")
    st.caption("¿Qué comportamientos o actitudes tiene este líder en su comunicación y trato diario que consideras muy valiosos y debería seguir haciendo?")
    resp_continuar = st.text_area("Tu respuesta", height=130, key="continuar", label_visibility="collapsed")

    st.markdown("### 🔴 Dejar de hacer")
    st.caption('¿Qué acciones o formas de comunicarse están generando "ruido", desmotivación o cuellos de botella en el equipo y debería detener?')
    resp_dejar = st.text_area("Tu respuesta", height=130, key="dejar", label_visibility="collapsed")

    st.markdown("### 🔵 Empezar a hacer")
    st.caption(f"Pensando en los desafíos del área de {evaluado_area}, ¿qué acción específica le recomendarías incorporar para mejorar su liderazgo, la forma en que reconoce al equipo o cómo entrega feedback?")
    resp_empezar = st.text_area("Tu respuesta", height=130, key="empezar", label_visibility="collapsed")

    st.divider()
    enviado = st.form_submit_button("Enviar respuestas ✅", use_container_width=True)

if enviado:
    if not resp_continuar.strip() and not resp_dejar.strip() and not resp_empezar.strip():
        st.error("Por favor responde al menos una pregunta antes de enviar.")
    else:
        queries.cc_guardar_respuestas(
            evaluador["id"],
            resp_continuar.strip() or None,
            resp_dejar.strip()     or None,
            resp_empezar.strip()   or None,
        )
        st.success(f"¡Gracias, {evaluador['nombre']}! Tus respuestas fueron enviadas.")
        st.balloons()
        st.rerun()
