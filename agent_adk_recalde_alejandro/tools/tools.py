"""Herramientas del asistente de estudio de la materia de Agentes de IA.

Cada función es una tool de ADK: el docstring es lo que lee el modelo para
decidir cuándo usarla. Todas validan sus argumentos y devuelven un texto
legible (nunca lanzan excepciones hacia el agente).
"""

import chromadb
from ddgs import DDGS
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pathlib import Path

# Ruta absoluta: el agente puede lanzarse desde otra carpeta (adk web desde el padre).
PERSIST_DIR = str(Path(__file__).resolve().parents[1] / "vector_store")
COLLECTION = "apuntes_materia"
MAX_RESULTADOS = 10


def _limitar(valor, defecto, minimo=1, maximo=MAX_RESULTADOS):
    """Convierte y recorta un entero al rango [minimo, maximo]."""
    try:
        return max(minimo, min(int(valor), maximo))
    except (TypeError, ValueError):
        return defecto


def _store(collection_name=COLLECTION):
    return Chroma(
        embedding_function=OllamaEmbeddings(model="nomic-embed-text"),
        persist_directory=PERSIST_DIR,
        collection_name=collection_name,
    )


def buscar_apuntes(consulta: str, k: int = 4) -> str:
    """Busca fragmentos relevantes en los apuntes de la materia (base vectorial).

    Args:
        consulta: tema o pregunta a buscar, por ejemplo "que es un agente de IA".
        k: cantidad de fragmentos a devolver, entre 1 y 10.

    Returns:
        Los fragmentos encontrados con su fuente y relevancia, o un mensaje
        de error si la consulta es inválida o no hay resultados.
    """
    consulta = (consulta or "").strip()
    if not consulta:
        return "Error: la consulta no puede estar vacía."
    k = _limitar(k, 4)

    try:
        results = _store().similarity_search_with_relevance_scores(consulta, k=k)
    except Exception as e:
        return f"Error al consultar la base vectorial: {e}"

    fragmentos = [
        f"[{doc.metadata.get('source', 'apunte')} | relevancia {score:.2f}]\n"
        f"{doc.page_content.strip()}"
        for doc, score in results
        if score is not None
    ]
    if not fragmentos:
        return f"No se encontraron resultados para '{consulta}' en los apuntes."
    return "\n\n".join(fragmentos)


def indexar_apunte(texto: str, titulo: str = "apunte") -> str:
    """Guarda un texto nuevo en la base vectorial de apuntes para consultarlo después.

    Args:
        texto: contenido a guardar (mínimo 20 caracteres).
        titulo: nombre corto con el que se identificará el apunte.

    Returns:
        Confirmación con la cantidad de fragmentos guardados, o un mensaje de error.
    """
    texto = (texto or "").strip()
    titulo = (titulo or "").strip() or "apunte"
    if not texto:
        return "Error: el texto a indexar no puede estar vacío."
    if len(texto) < 20:
        return "Error: el texto es demasiado corto para indexar (mínimo 20 caracteres)."

    try:
        splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        docs = splitter.create_documents([texto], metadatas=[{"source": titulo}])
        ids = _store().add_documents(docs)
    except Exception as e:
        return f"Error al indexar el apunte: {e}"

    if not ids:
        return "No se pudo indexar el texto: no se generaron fragmentos."
    return f"Guardado '{titulo}' en {len(ids)} fragmento(s) de la colección {COLLECTION}."


def buscar_en_internet(consulta: str, max_resultados: int = 5) -> str:
    """Busca información actualizada en internet (DuckDuckGo).

    Args:
        consulta: consulta para el buscador.
        max_resultados: cantidad máxima de resultados, entre 1 y 10.

    Returns:
        Los resultados con título, resumen y URL, o un mensaje de error.
    """
    consulta = (consulta or "").strip()
    if not consulta:
        return "Error: la consulta no puede estar vacía."
    max_resultados = _limitar(max_resultados, 5)

    # ddgs a veces falla por rate limit; un segundo intento suele resolverlo.
    results, ultimo_error = None, ""
    for _ in range(2):
        try:
            results = DDGS().text(query=consulta, max_results=max_resultados)
            break
        except Exception as e:
            ultimo_error = e
    if results is None:
        return f"Error al buscar en internet: {ultimo_error}"

    if not results:
        return f"No se encontraron resultados en internet para '{consulta}'."

    lineas = []
    for i, r in enumerate(results, 1):
        lineas.append(
            f"{i}. {r.get('title', 'Sin título')}\n"
            f"{r.get('body', 'Sin resumen')}\n"
            f"{r.get('href', 'Sin URL')}"
        )
    return "\n\n".join(lineas)


def listar_colecciones() -> str:
    """Lista las colecciones disponibles en la base de datos vectorial.

    Returns:
        Nombres de las colecciones existentes, o un mensaje de error.
    """
    try:
        client = chromadb.PersistentClient(path=PERSIST_DIR)
        nombres = [c.name for c in client.list_collections()]
    except Exception as e:
        return f"Error al listar las colecciones: {e}"

    if not nombres:
        return "No hay colecciones creadas todavía. Indexá apuntes primero."
    return "Colecciones disponibles: " + ", ".join(nombres)
