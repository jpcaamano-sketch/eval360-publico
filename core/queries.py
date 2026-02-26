"""Operaciones de base de datos para Evaluación 360 v2."""

import functools
from core.database import get_client, ejecutar_con_reintento


def con_reintento(fn):
    """Decorador que reintenta la función ante errores SSL/conexión."""
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        return ejecutar_con_reintento(lambda: fn(*args, **kwargs))
    return wrapper


# ============================================================
# PLANTILLAS
# ============================================================

@con_reintento
def listar_plantillas(solo_activas=False):
    """Lista todas las plantillas."""
    sb = get_client()
    q = sb.table("v2_plantillas").select("*").order("nombre")
    if solo_activas:
        q = q.eq("activa", True)
    return q.execute().data


@con_reintento
def obtener_plantilla(plantilla_id):
    """Obtiene una plantilla por ID."""
    sb = get_client()
    res = sb.table("v2_plantillas").select("*").eq("id", plantilla_id).execute()
    return res.data[0] if res.data else None


@con_reintento
def crear_plantilla(nombre, descripcion=""):
    """Crea una nueva plantilla."""
    sb = get_client()
    return sb.table("v2_plantillas").insert({
        "nombre": nombre,
        "descripcion": descripcion,
    }).execute().data[0]


@con_reintento
def actualizar_plantilla(plantilla_id, datos):
    """Actualiza campos de una plantilla."""
    sb = get_client()
    return sb.table("v2_plantillas").update(datos).eq("id", plantilla_id).execute()


@con_reintento
def eliminar_plantilla(plantilla_id):
    """Elimina una plantilla (cascade borra categorías y competencias)."""
    sb = get_client()
    return sb.table("v2_plantillas").delete().eq("id", plantilla_id).execute()


# ============================================================
# CATEGORÍAS
# ============================================================

@con_reintento
def listar_categorias(plantilla_id):
    """Lista categorías de una plantilla ordenadas."""
    sb = get_client()
    return sb.table("v2_categorias").select("*").eq(
        "plantilla_id", plantilla_id
    ).order("orden").execute().data


@con_reintento
def crear_categoria(plantilla_id, nombre, orden=0):
    """Crea una categoría."""
    sb = get_client()
    return sb.table("v2_categorias").insert({
        "plantilla_id": plantilla_id,
        "nombre": nombre,
        "orden": orden,
    }).execute().data[0]


@con_reintento
def actualizar_categoria(categoria_id, datos):
    """Actualiza una categoría."""
    sb = get_client()
    return sb.table("v2_categorias").update(datos).eq("id", categoria_id).execute()


@con_reintento
def eliminar_categoria(categoria_id):
    """Elimina una categoría (cascade borra competencias)."""
    sb = get_client()
    return sb.table("v2_categorias").delete().eq("id", categoria_id).execute()


# ============================================================
# COMPETENCIAS
# ============================================================

@con_reintento
def listar_competencias(categoria_id):
    """Lista competencias de una categoría ordenadas."""
    sb = get_client()
    return sb.table("v2_competencias").select("*").eq(
        "categoria_id", categoria_id
    ).order("orden").execute().data


@con_reintento
def listar_competencias_por_plantilla(plantilla_id):
    """Lista todas las competencias de una plantilla con su categoría."""
    categorias = listar_categorias(plantilla_id)
    resultado = []
    for cat in categorias:
        comps = listar_competencias(cat["id"])
        for comp in comps:
            comp["categoria_nombre"] = cat["nombre"]
        resultado.extend(comps)
    return resultado


@con_reintento
def crear_competencia(categoria_id, texto_auto, texto_feedback, orden=0):
    """Crea una competencia."""
    sb = get_client()
    return sb.table("v2_competencias").insert({
        "categoria_id": categoria_id,
        "texto_auto": texto_auto,
        "texto_feedback": texto_feedback,
        "orden": orden,
    }).execute().data[0]


@con_reintento
def actualizar_competencia(competencia_id, datos):
    """Actualiza una competencia."""
    sb = get_client()
    return sb.table("v2_competencias").update(datos).eq("id", competencia_id).execute()


@con_reintento
def eliminar_competencia(competencia_id):
    """Elimina una competencia."""
    sb = get_client()
    return sb.table("v2_competencias").delete().eq("id", competencia_id).execute()


# ============================================================
# GRUPOS
# ============================================================

@con_reintento
def contar_grupos_por_plantilla(plantilla_id):
    """Retorna la cantidad de grupos que usan esta plantilla."""
    sb = get_client()
    res = sb.table("v2_grupos").select("id", count="exact").eq("plantilla_id", plantilla_id).execute()
    return res.count or 0


@con_reintento
def listar_grupos():
    """Lista todos los grupos con info de plantilla (1 sola query con join)."""
    sb = get_client()
    return sb.table("v2_grupos").select(
        "*, v2_plantillas(nombre)"
    ).order("created_at", desc=True).execute().data or []


@con_reintento
def obtener_grupo(grupo_id):
    """Obtiene un grupo por ID con info de plantilla (1 sola query con join)."""
    sb = get_client()
    res = sb.table("v2_grupos").select(
        "*, v2_plantillas(nombre)"
    ).eq("id", grupo_id).execute()
    return res.data[0] if res.data else None


@con_reintento
def crear_grupo(nombre, plantilla_id):
    """Crea un nuevo grupo."""
    sb = get_client()
    return sb.table("v2_grupos").insert({
        "nombre": nombre,
        "plantilla_id": plantilla_id,
    }).execute().data[0]


@con_reintento
def actualizar_grupo(grupo_id, datos):
    """Actualiza campos de un grupo."""
    sb = get_client()
    return sb.table("v2_grupos").update(datos).eq("id", grupo_id).execute()


@con_reintento
def eliminar_grupo(grupo_id):
    """Elimina un grupo (cascade borra participantes y evaluadores)."""
    sb = get_client()
    return sb.table("v2_grupos").delete().eq("id", grupo_id).execute()


# ============================================================
# PARTICIPANTES
# ============================================================

@con_reintento
def listar_participantes(grupo_id):
    """Lista participantes de un grupo."""
    sb = get_client()
    return sb.table("v2_participantes").select("*").eq(
        "grupo_id", grupo_id
    ).order("correlativo").execute().data


@con_reintento
def obtener_participante_por_token(token):
    """Obtiene un participante por su token de autoevaluación, con datos del grupo."""
    sb = get_client()
    res = sb.table("v2_participantes").select("*").eq("token_auto", token).execute()
    if not res.data:
        return None
    participante = res.data[0]
    grupo_res = sb.table("v2_grupos").select("*").eq("id", participante["grupo_id"]).execute()
    if grupo_res.data:
        participante["v2_grupos"] = grupo_res.data[0]
    return participante


@con_reintento
def crear_participante(grupo_id, nombre, email):
    """Crea un participante."""
    sb = get_client()
    return sb.table("v2_participantes").insert({
        "grupo_id": grupo_id,
        "nombre": nombre,
        "email": email,
    }).execute().data[0]


@con_reintento
def actualizar_participante(participante_id, datos):
    """Actualiza campos de un participante."""
    sb = get_client()
    return sb.table("v2_participantes").update(datos).eq("id", participante_id).execute()


@con_reintento
def eliminar_participante(participante_id):
    """Elimina un participante."""
    sb = get_client()
    return sb.table("v2_participantes").delete().eq("id", participante_id).execute()


# ============================================================
# EVALUADORES
# ============================================================

@con_reintento
def listar_evaluadores(participante_id):
    """Lista evaluadores de un participante."""
    sb = get_client()
    return sb.table("v2_evaluadores").select("*").eq(
        "participante_id", participante_id
    ).order("created_at").execute().data


@con_reintento
def listar_evaluadores_por_grupo(grupo_id):
    """Lista todos los evaluadores de un grupo."""
    participantes = listar_participantes(grupo_id)
    evaluadores = []
    for p in participantes:
        evs = listar_evaluadores(p["id"])
        for ev in evs:
            ev["participante_nombre"] = p["nombre"]
            ev["participante_email"] = p["email"]
            ev["participante_id_ref"] = p["id"]
        evaluadores.extend(evs)
    return evaluadores


@con_reintento
def obtener_evaluador_por_token(token):
    """Obtiene un evaluador por su token, con datos del participante y grupo."""
    sb = get_client()
    res = sb.table("v2_evaluadores").select("*").eq("token", token).execute()
    if not res.data:
        return None
    evaluador = res.data[0]
    part_res = sb.table("v2_participantes").select("*").eq("id", evaluador["participante_id"]).execute()
    if part_res.data:
        participante = part_res.data[0]
        grupo_res = sb.table("v2_grupos").select("*").eq("id", participante["grupo_id"]).execute()
        if grupo_res.data:
            participante["v2_grupos"] = grupo_res.data[0]
        evaluador["v2_participantes"] = participante
    return evaluador


@con_reintento
def crear_evaluador(participante_id, nombre, email):
    """Crea un evaluador."""
    sb = get_client()
    return sb.table("v2_evaluadores").insert({
        "participante_id": participante_id,
        "nombre": nombre,
        "email": email,
    }).execute().data[0]


@con_reintento
def actualizar_evaluador(evaluador_id, datos):
    """Actualiza campos de un evaluador."""
    sb = get_client()
    return sb.table("v2_evaluadores").update(datos).eq("id", evaluador_id).execute()


@con_reintento
def eliminar_evaluador(evaluador_id):
    """Elimina un evaluador."""
    sb = get_client()
    return sb.table("v2_evaluadores").delete().eq("id", evaluador_id).execute()


# ============================================================
# RESPUESTAS
# ============================================================

@con_reintento
def guardar_respuestas_auto(participante_id, respuestas_dict):
    """Guarda respuestas de autoevaluación.
    respuestas_dict: {competencia_id: puntaje}
    """
    sb = get_client()
    registros = [
        {
            "participante_id": participante_id,
            "evaluador_id": None,
            "competencia_id": comp_id,
            "puntaje": puntaje,
            "es_autoevaluacion": True,
        }
        for comp_id, puntaje in respuestas_dict.items()
    ]
    return sb.table("v2_respuestas").insert(registros).execute()


@con_reintento
def guardar_respuestas_feedback(participante_id, evaluador_id, respuestas_dict):
    """Guarda respuestas de feedback.
    respuestas_dict: {competencia_id: puntaje}
    """
    sb = get_client()
    registros = [
        {
            "participante_id": participante_id,
            "evaluador_id": evaluador_id,
            "competencia_id": comp_id,
            "puntaje": puntaje,
            "es_autoevaluacion": False,
        }
        for comp_id, puntaje in respuestas_dict.items()
    ]
    return sb.table("v2_respuestas").insert(registros).execute()


@con_reintento
def obtener_respuestas_participante(participante_id):
    """Obtiene todas las respuestas para un participante."""
    sb = get_client()
    return sb.table("v2_respuestas").select("*").eq(
        "participante_id", participante_id
    ).execute().data
