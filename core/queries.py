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
# HELPERS DE ENRIQUECIMIENTO
# ============================================================

def _enriquecer_participante(p):
    """Añade nombre/email virtuales desde sist_personas para compatibilidad."""
    sp = p.pop("sist_personas", None) or {}
    p["pers_nombres"] = sp.get("pers_nombres", "")
    p["pers_apellidos"] = sp.get("pers_apellidos", "")
    p["pers_correo"] = sp.get("pers_correo") or ""
    nombres = p["pers_nombres"]
    apellidos = p["pers_apellidos"]
    p["nombre"] = f"{nombres} {apellidos}".strip() or p.get("pers_rut") or "—"
    p["email"] = p["pers_correo"]
    return p


def _enriquecer_grupo(g, empresa_map=None):
    """Añade empresa virtual desde otec_empresas para compatibilidad."""
    # Limpia el join embebido si existiera (ignorado)
    g.pop("otec_empresas", None)
    if empresa_map:
        nombre_emp = empresa_map.get(g.get("rut_empresa") or "", "") or ""
    else:
        nombre_emp = ""
    g["empresa_nombre"] = nombre_emp
    g["empresa"] = nombre_emp
    return g


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
# PERSONAS (sist_personas) y EMPRESAS (otec_empresas)
# ============================================================

@con_reintento
def listar_empresas_otec():
    """Lista todas las empresas de otec_empresas ordenadas por nombre."""
    sb = get_client()
    return sb.table("otec_empresas").select(
        "rut_empresa, nombre_empresa"
    ).order("nombre_empresa").execute().data or []


@con_reintento
def listar_personas_sist(rut_empresa=None, solo_con_correo=True):
    """Lista personas de sist_personas.
    Si rut_empresa se pasa, filtra por esa empresa.
    Si solo_con_correo=True (default), excluye personas sin correo."""
    sb = get_client()
    q = sb.table("sist_personas").select(
        "pers_rut, pers_nombres, pers_apellidos, pers_correo, rut_empresa"
    )
    if rut_empresa:
        q = q.eq("rut_empresa", rut_empresa)
    res = q.order("pers_apellidos").execute().data or []
    if solo_con_correo:
        return [p for p in res if p.get("pers_correo")]
    return res


@con_reintento
def crear_persona_sist(pers_rut, nombres, apellidos, correo, rut_empresa=None):
    """Crea o actualiza una persona en sist_personas."""
    sb = get_client()
    datos = {
        "pers_rut": pers_rut,
        "pers_nombres": nombres,
        "pers_apellidos": apellidos,
        "pers_correo": correo,
    }
    if rut_empresa:
        datos["rut_empresa"] = rut_empresa
    return sb.table("sist_personas").upsert(datos, on_conflict="pers_rut").execute()


@con_reintento
def buscar_persona_por_correo(correo):
    """Busca una persona en sist_personas por correo electrónico."""
    sb = get_client()
    res = sb.table("sist_personas").select(
        "pers_rut, pers_nombres, pers_apellidos, pers_correo"
    ).eq("pers_correo", correo).limit(1).execute()
    return res.data[0] if res.data else None


@con_reintento
def actualizar_persona_sist(pers_rut, datos):
    """Actualiza datos de una persona en sist_personas."""
    sb = get_client()
    return sb.table("sist_personas").update(datos).eq("pers_rut", pers_rut).execute()


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
    """Lista todos los grupos con info de plantilla y empresa."""
    sb = get_client()
    res = sb.table("v2_grupos").select(
        "*, v2_plantillas(nombre)"
    ).order("created_at", desc=True).execute()
    grupos = res.data or []
    if grupos:
        emp_res = sb.table("otec_empresas").select("rut_empresa, nombre_empresa").execute()
        empresa_map = {e["rut_empresa"]: e["nombre_empresa"] for e in (emp_res.data or [])}
        return [_enriquecer_grupo(g, empresa_map) for g in grupos]
    return grupos


@con_reintento
def obtener_grupo(grupo_id):
    """Obtiene un grupo por ID con info de plantilla y empresa."""
    sb = get_client()
    res = sb.table("v2_grupos").select(
        "*, v2_plantillas(nombre)"
    ).eq("id", grupo_id).execute()
    if not res.data:
        return None
    g = res.data[0]
    rut = g.get("rut_empresa") or ""
    nombre_emp = ""
    if rut:
        emp_res = sb.table("otec_empresas").select("nombre_empresa").eq("rut_empresa", rut).execute()
        nombre_emp = emp_res.data[0]["nombre_empresa"] if emp_res.data else ""
    g["empresa_nombre"] = nombre_emp
    g["empresa"] = nombre_emp
    return g


@con_reintento
def crear_grupo(nombre, plantilla_id, rut_empresa=None):
    """Crea un nuevo grupo."""
    sb = get_client()
    return sb.table("v2_grupos").insert({
        "nombre": nombre,
        "plantilla_id": plantilla_id,
        "rut_empresa": rut_empresa,
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
    """Lista participantes de un grupo con datos de sist_personas."""
    sb = get_client()
    res = sb.table("v2_participantes").select(
        "*, sist_personas(pers_nombres, pers_apellidos, pers_correo)"
    ).eq("grupo_id", grupo_id).execute()
    participantes = [_enriquecer_participante(p) for p in (res.data or [])]
    return sorted(participantes, key=lambda p: p.get("pers_apellidos", "").lower())


@con_reintento
def obtener_participante_por_token(token):
    """Obtiene un participante por su token de autoevaluación, con datos del grupo y sist_personas."""
    sb = get_client()
    res = sb.table("v2_participantes").select(
        "*, sist_personas(pers_nombres, pers_apellidos, pers_correo)"
    ).eq("token_auto", token).execute()
    if not res.data:
        return None
    participante = _enriquecer_participante(res.data[0])
    grupo_res = sb.table("v2_grupos").select("*").eq("id", participante["grupo_id"]).execute()
    if grupo_res.data:
        participante["v2_grupos"] = grupo_res.data[0]
    return participante


@con_reintento
def crear_participante(grupo_id, pers_rut):
    """Crea un participante vinculado a sist_personas por pers_rut."""
    sb = get_client()
    return sb.table("v2_participantes").insert({
        "grupo_id": grupo_id,
        "pers_rut": pers_rut,
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
    part_res = sb.table("v2_participantes").select(
        "*, sist_personas(pers_nombres, pers_apellidos, pers_correo)"
    ).eq("id", evaluador["participante_id"]).execute()
    if part_res.data:
        participante = _enriquecer_participante(part_res.data[0])
        grupo_res = sb.table("v2_grupos").select("*").eq("id", participante["grupo_id"]).execute()
        if grupo_res.data:
            participante["v2_grupos"] = grupo_res.data[0]
        evaluador["v2_participantes"] = participante
    return evaluador


@con_reintento
def crear_evaluador(participante_id, nombre, email, pers_rut=None):
    """Crea un evaluador. pers_rut opcional: se vincula a sist_personas si se conoce."""
    sb = get_client()
    datos = {
        "participante_id": participante_id,
        "nombre": nombre,
        "email": email,
    }
    if pers_rut:
        datos["pers_rut"] = pers_rut
    return sb.table("v2_evaluadores").insert(datos).execute().data[0]


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


@con_reintento
def eliminar_respuestas_auto(participante_id):
    """Elimina todas las respuestas de autoevaluación de un participante."""
    sb = get_client()
    return sb.table("v2_respuestas").delete().eq(
        "participante_id", participante_id
    ).eq("es_autoevaluacion", True).execute()


@con_reintento
def eliminar_respuestas_feedback(participante_id, evaluador_id):
    """Elimina respuestas de feedback de un evaluador para un participante."""
    sb = get_client()
    return sb.table("v2_respuestas").delete().eq(
        "participante_id", participante_id
    ).eq("evaluador_id", evaluador_id).execute()
