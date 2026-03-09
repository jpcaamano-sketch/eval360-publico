"""
Evaluación 360 v2 — Formulario de Feedback
Puerto: 8508
Acceso público con token de evaluador.
"""

import random
import streamlit as st
from datetime import datetime, timezone
from core.config import ESCALA
from core.styles import FEEDBACK_CSS
from core import queries

st.set_page_config(page_title="Feedback 360°", page_icon="💬", layout="centered")
st.markdown(FEEDBACK_CSS, unsafe_allow_html=True)

ESCALA_OPCIONES = list(ESCALA.values())

# ============================================================
# OBTENER TOKEN
# ============================================================

token = st.query_params.get("token")

if not token:
    pass  # titulo removido
    st.warning("Acceso no válido. Utiliza el enlace que recibiste por email.")
    st.stop()

# ============================================================
# VALIDAR EVALUADOR
# ============================================================

evaluador = queries.obtener_evaluador_por_token(token)

if not evaluador:
    pass  # titulo removido
    st.error("Token no válido o expirado.")
    st.stop()

if evaluador["completado"]:
    pass  # titulo removido
    st.success(f"¡Gracias, {evaluador['nombre']}! Tu evaluación ya fue completada.")
    st.balloons()
    st.stop()

# ============================================================
# OBTENER DATOS
# ============================================================

participante_info = evaluador.get("v2_participantes", {})
participante_nombre = participante_info.get("nombre", "el participante") if participante_info else "el participante"
participante_id = participante_info.get("id") if participante_info else None
grupo_info = participante_info.get("v2_grupos", {}) if participante_info else {}
plantilla_id = grupo_info.get("plantilla_id") if grupo_info else None

if not plantilla_id or not participante_id:
    st.error("Error de configuración: no se encontró la información del evaluado.")
    st.stop()

competencias = queries.listar_competencias_por_plantilla(plantilla_id)

if not competencias:
    st.error("La plantilla no tiene competencias configuradas.")
    st.stop()

# ============================================================
# FORMULARIO TIPO TABLA
# ============================================================


st.title("Feedback 360°")
st.markdown(f"**Hola, {evaluador['nombre']}**")
st.markdown(f"Estás evaluando a **{participante_nombre}**. Tu feedback es **anónimo**.")
st.markdown("Responde según la frecuencia con la que observas la conducta.")
st.divider()

# Orden fijo según plantilla
competencias_shuffle = list(competencias)

# Cabecera de tabla
hc = st.columns([0.4, 3.5, 0.9, 0.9, 0.9, 1.2, 0.9])
hc[0].markdown("**#**")
hc[1].markdown("**Competencia**")
hc[2].markdown("**Nunca**")
hc[3].markdown("**Rara vez**")
hc[4].markdown("**A veces**")
hc[5].markdown("**Frecuent.**")
hc[6].markdown("**Siempre**")
st.markdown("---")

respuestas = {}
todas_respondidas = True


def make_fb_callback(cid, val):
    """Callback para exclusión mutua: al marcar una opción, desmarca las demás."""
    def cb():
        if st.session_state.get(f"fb_{cid}_{val}"):
            for v in range(1, 6):
                if v != val:
                    st.session_state[f"fb_{cid}_{v}"] = False
    return cb


for idx, comp in enumerate(competencias_shuffle, 1):
    cid = comp["id"]
    rc = st.columns([0.4, 3.5, 0.9, 0.9, 0.9, 1.2, 0.9])
    with rc[0]:
        st.markdown(f"**{idx}**")
    with rc[1]:
        st.markdown(comp["texto_feedback"])
    for col_idx, val in enumerate(range(1, 6)):
        with rc[col_idx + 2]:
            st.checkbox(
                " ",
                key=f"fb_{cid}_{val}",
                on_change=make_fb_callback(cid, val),
                label_visibility="hidden",
            )
    sel_val = None
    for v in range(1, 6):
        if st.session_state.get(f"fb_{cid}_{v}"):
            sel_val = v
            break
    if sel_val is not None:
        respuestas[cid] = sel_val
    else:
        todas_respondidas = False

st.divider()

# ============================================================
# GUARDAR
# ============================================================

if st.button("Enviar Evaluación", use_container_width=True, type="primary"):
    if not todas_respondidas or len(respuestas) < len(competencias):
        st.error("Debes responder todas las competencias antes de enviar.")
    else:
        try:
            queries.guardar_respuestas_feedback(participante_id, evaluador["id"], respuestas)

            queries.actualizar_evaluador(evaluador["id"], {
                "completado": True,
                "fecha_completado": datetime.now(timezone.utc).isoformat(),
            })

            st.success("¡Tu evaluación ha sido guardada exitosamente! Gracias por tu feedback.")
            st.balloons()
            st.rerun()

        except Exception as e:
            st.error(f"Error al guardar: {e}")
