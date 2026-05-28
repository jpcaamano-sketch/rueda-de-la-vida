import uuid
from supabase import create_client, Client
from core.config import SUPABASE_URL, SUPABASE_KEY

_client: Client = None

def get_db() -> Client:
    global _client
    if _client is None:
        _client = create_client(SUPABASE_URL, SUPABASE_KEY)
    return _client


# ─── Participantes ────────────────────────────────────────────────────────

def crear_participante(nombre: str, email: str) -> dict:
    """Crea un nuevo participante con token único. Retorna el registro."""
    token = str(uuid.uuid4())
    data = get_db().table("rueda_participantes").insert({
        "nombre":     nombre,
        "email":      email,
        "token":      token,
        "completado": False,
    }).execute()
    return data.data[0]


def get_participante_por_token(token: str) -> dict | None:
    data = get_db().table("rueda_participantes") \
        .select("*").eq("token", token).execute()
    return data.data[0] if data.data else None


def get_participante_por_email(email: str) -> dict | None:
    data = get_db().table("rueda_participantes") \
        .select("*").eq("email", email).order("created_at", desc=True).limit(1).execute()
    return data.data[0] if data.data else None


def marcar_completado(participante_id: str):
    from datetime import datetime, timezone
    get_db().table("rueda_participantes").update({
        "completado":    True,
        "completado_at": datetime.now(timezone.utc).isoformat(),
    }).eq("id", participante_id).execute()


def listar_participantes() -> list:
    data = get_db().table("rueda_participantes") \
        .select("*").order("created_at", desc=True).execute()
    return data.data or []


# ─── Respuestas ───────────────────────────────────────────────────────────

def guardar_respuestas(participante_id: str, respuestas: dict):
    """
    respuestas: {"1.1": 7, "1.2": 9, ...}
    """
    rows = [
        {"participante_id": participante_id, "comportamiento_id": comp_id, "puntaje": puntaje}
        for comp_id, puntaje in respuestas.items()
    ]
    get_db().table("rueda_respuestas").insert(rows).execute()


def get_respuestas(participante_id: str) -> dict:
    """Retorna dict {comportamiento_id: puntaje}"""
    data = get_db().table("rueda_respuestas") \
        .select("comportamiento_id, puntaje").eq("participante_id", participante_id).execute()
    return {r["comportamiento_id"]: r["puntaje"] for r in (data.data or [])}
