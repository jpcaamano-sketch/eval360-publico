"""
Evaluación 360 v2 — Formulario de Autoevaluación
Puerto: 8507
Acceso público con token.
"""

import random
import streamlit as st
from core.config import ESCALA
from core.styles import AUTO_CSS
from core import queries

st.set_page_config(page_title="Autoevaluación 360°", page_icon="📝", layout="centered")
st.markdown(AUTO_CSS, unsafe_allow_html=True)

ESCALA_OPCIONES = list(ESCALA.values())  # ["Nunca", "Rara vez", "A veces", "Frecuentemente", "Siempre"]

# ============================================================
# OBTENER TOKEN
# ============================================================

token = st.query_params.get("token")

if not token:
    pass  # titulo removido
    st.warning("Acceso no válido. Utiliza el enlace que recibiste por email.")
    st.stop()

# ============================================================
# VALIDAR PARTICIPANTE
# ============================================================

participante = queries.obtener_participante_por_token(token)

if not participante:
    pass  # titulo removido
    st.error("Token no válido o expirado.")
    st.stop()

if participante["autoevaluacion_completada"]:
    pass  # titulo removido
    st.success(f"¡Gracias, {participante.get('nombre', '')}! Tu autoevaluación ya fue completada.")
    st.balloons()
    st.stop()

# ============================================================
# OBTENER COMPETENCIAS
# ============================================================

grupo = participante.get("v2_grupos", {})
plantilla_id = grupo.get("plantilla_id") if grupo else None

if not plantilla_id:
    st.error("Error de configuración: no se encontró la plantilla asociada.")
    st.stop()

competencias = queries.listar_competencias_por_plantilla(plantilla_id)

if not competencias:
    st.error("La plantilla no tiene competencias configuradas.")
    st.stop()

# ============================================================
# FORMULARIO TIPO TABLA
# ============================================================


st.title("Autoevaluación 360°")
st.markdown(f"**Hola, {participante.get('nombre', '')}**")
st.markdown("Responde cada afirmación según la frecuencia con la que aplica a ti. Y anotar los datos de las personas que te evaluarán.")
st.divider()

# Orden fijo según plantilla
competencias_shuffle = list(competencias)

# Cabecera de tabla
hc = st.columns([0.4, 5.0, 0.7, 0.7, 0.7, 0.9, 0.7])
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


def make_auto_callback(cid, val):
    """Callback para exclusión mutua: al marcar una opción, desmarca las demás."""
    def cb():
        if st.session_state.get(f"auto_{cid}_{val}"):
            for v in range(1, 6):
                if v != val:
                    st.session_state[f"auto_{cid}_{v}"] = False
    return cb


for idx, comp in enumerate(competencias_shuffle, 1):
    cid = comp["id"]
    rc = st.columns([0.4, 5.0, 0.7, 0.7, 0.7, 0.9, 0.7])
    with rc[0]:
        st.markdown(f"**{idx}**")
    with rc[1]:
        st.markdown(comp["texto_auto"])
    for col_idx, val in enumerate(range(1, 6)):
        with rc[col_idx + 2]:
            st.checkbox(
                " ",
                key=f"auto_{cid}_{val}",
                on_change=make_auto_callback(cid, val),
                label_visibility="hidden",
            )
    sel_val = None
    for v in range(1, 6):
        if st.session_state.get(f"auto_{cid}_{v}"):
            sel_val = v
            break
    if sel_val is not None:
        respuestas[cid] = sel_val
    else:
        todas_respondidas = False

st.divider()

# ============================================================
# SECCIÓN DE EVALUADORES (3 a 5)
# ============================================================

st.subheader("Evaluadores")
st.markdown(
    "Ingresa entre **3 y 5** personas que te evaluarán. "
    "Deben ser colegas, supervisores o colaboradores que te conozcan bien."
)

NUM_EVAL_SLOTS = 5
evaluadores_data = []

for i in range(NUM_EVAL_SLOTS):
    obligatorio = " *(obligatorio)*" if i < 3 else " *(opcional)*"
    st.markdown(f"**Evaluador {i + 1}**{obligatorio}")
    col1, col2 = st.columns(2)
    with col1:
        nombre_ev = st.text_input(f"Nombre", key=f"ev_nombre_{i}", label_visibility="hidden",
                                   placeholder=f"Nombre evaluador {i + 1}")
    with col2:
        email_ev = st.text_input(f"Email", key=f"ev_email_{i}", label_visibility="hidden",
                                  placeholder=f"Email evaluador {i + 1}")
    if nombre_ev.strip() and email_ev.strip():
        evaluadores_data.append({"nombre": nombre_ev.strip(), "email": email_ev.strip()})

st.divider()

# ============================================================
# GUARDAR
# ============================================================

if st.button("Guardar Autoevaluación", use_container_width=True, type="primary"):
    errores = []

    if not todas_respondidas or len(respuestas) < len(competencias):
        errores.append("Debes responder todas las competencias.")

    if len(evaluadores_data) < 3:
        errores.append("¡¡Falta nombres de colaboradores!! Debes ingresar al menos 3 evaluadores.")

    if errores:
        for err in errores:
            st.error(err)
    else:
        try:
            queries.guardar_respuestas_auto(participante["id"], respuestas)

            for ev in evaluadores_data:
                persona = queries.buscar_persona_por_correo(ev["email"])
                pers_rut = persona["pers_rut"] if persona else None
                queries.crear_evaluador(participante["id"], ev["nombre"], ev["email"], pers_rut)

            from datetime import datetime, timezone
            queries.actualizar_participante(participante["id"], {
                "autoevaluacion_completada": True,
                "autoevaluacion_fecha": datetime.now(timezone.utc).isoformat(),
            })

            st.success("¡Tu autoevaluación ha sido guardada exitosamente! Gracias por participar.")
            st.balloons()
            st.rerun()

        except Exception as e:
            st.error(f"Error al guardar: {e}")
