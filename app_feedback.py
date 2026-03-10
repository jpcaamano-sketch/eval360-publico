"""
Evaluación 360 v2 — Formulario de Feedback
Puerto: 8508
Acceso público con token de evaluador.
"""

import streamlit as st
from datetime import datetime, timezone
from core.config import ESCALA
from core.styles import FEEDBACK_CSS
from core import queries

st.set_page_config(page_title="Feedback 360°", page_icon="💬", layout="centered")
st.markdown(FEEDBACK_CSS, unsafe_allow_html=True)

# ============================================================
# OBTENER TOKEN
# ============================================================

token = st.query_params.get("token")

if not token:
    st.warning("Acceso no válido. Utiliza el enlace que recibiste por email.")
    st.stop()

# ============================================================
# VALIDAR EVALUADOR
# ============================================================

evaluador = queries.obtener_evaluador_por_token(token)

if not evaluador:
    st.error("Token no válido o expirado.")
    st.stop()

if evaluador["completado"]:
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
# FORMULARIO
# ============================================================

st.title("Feedback 360°")
st.markdown(f"**Hola, {evaluador['nombre']}** — Estás evaluando a **{participante_nombre}**. Tu feedback es **anónimo**.")
st.markdown("Responde según la frecuencia con la que observas la conducta.")
st.divider()

respuestas = {}
todas_respondidas = True

for idx, comp in enumerate(competencias, 1):
    cid = comp["id"]
    st.markdown(f"**{idx}.** {comp['texto_feedback']}")
    val = st.radio(
        label=f"r{idx}",
        options=[1, 2, 3, 4, 5],
        format_func=lambda v: ESCALA[v],
        key=f"fb_{cid}",
        horizontal=True,
        index=None,
        label_visibility="collapsed",
    )
    if val is not None:
        respuestas[cid] = val
    else:
        todas_respondidas = False
    st.markdown("---")

st.divider()

# ============================================================
# GUARDAR
# ============================================================

if st.button("Guardar Feedback", use_container_width=True, type="primary"):
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
