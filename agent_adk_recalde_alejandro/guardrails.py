"""Guardrails del agente: bloquean solicitudes fuera de alcance antes del modelo."""

import re
import unicodedata

from google.genai import types

MENSAJE_RECHAZO = (
    "No puedo responder ese tipo de solicitud. Soy un asistente de estudio de la "
    "materia Agentes de Inteligencia Artificial: puedo consultar los apuntes, buscar "
    "información en internet sobre el tema o guardar apuntes nuevos."
)

# Patrones sobre el texto normalizado (minúsculas y sin tildes).
PATRONES_BLOQUEADOS = [
    # intentos de extraer instrucciones o saltarse las reglas
    r"(dame|mostra|revela|repeti|decime|escribi|copia|cual es).{0,40}(prompt|instrucciones)",
    r"(system|sistema).{0,10}prompt",
    r"prompt.{0,10}(system|sistema)",
    r"ignora.{0,15}(instrucciones|reglas)",
    r"jailbreak|modo desarrollador|sin restricciones|sin reglas",
    # temas ajenos a la materia
    r"presidente|politic|eleccion|gobierno|milei|kirchner|macri",
    r"receta|cocinar|cocina|huevo|ingredientes",
    r"clima|futbol|chiste|horoscopo|criptomoneda",
]


def _normalizar(texto: str) -> str:
    texto = unicodedata.normalize("NFD", (texto or "").lower())
    return "".join(c for c in texto if unicodedata.category(c) != "Mn")


def es_solicitud_bloqueada(texto: str) -> bool:
    """True si el mensaje es un intento de extraer el prompt o un tema ajeno a la materia."""
    normalizado = _normalizar(texto)
    return any(re.search(patron, normalizado) for patron in PATRONES_BLOQUEADOS)


def revisar_solicitud(callback_context):
    """before_agent_callback: responde el mensaje fijo sin llamar al modelo."""
    contenido = getattr(callback_context, "user_content", None)
    partes = getattr(contenido, "parts", None) or []
    texto = " ".join(p.text for p in partes if getattr(p, "text", None))

    if es_solicitud_bloqueada(texto):
        return types.Content(role="model", parts=[types.Part(text=MENSAJE_RECHAZO)])
    return None
