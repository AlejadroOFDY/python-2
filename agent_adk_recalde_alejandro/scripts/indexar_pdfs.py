"""Indexa los PDFs de data/ en la base vectorial de apuntes.

Uso (desde la raíz del repo):
    python scripts/indexar_pdfs.py
"""

import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ))

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pypdf import PdfReader

from tools.tools import COLLECTION, _store

PDFS = RAIZ / "data"


def leer_pdf(ruta: Path) -> str:
    texto = "\n".join(pagina.extract_text() or "" for pagina in PdfReader(str(ruta)).pages)
    # pypdf devuelve una palabra por línea en estos PDFs; se normaliza a prosa.
    return " ".join(texto.split())


def main() -> None:
    archivos = sorted(PDFS.glob("*.pdf"))
    if not archivos:
        print(f"No hay PDFs en {PDFS}. Copiá los apuntes ahí y volvé a ejecutar.")
        return

    documentos = []
    for ruta in archivos:
        texto = leer_pdf(ruta).strip()
        if not texto:
            print(f"AVISO: {ruta.name} no tiene texto extraíble, se omite.")
            continue
        documentos.append(Document(page_content=texto, metadata={"source": ruta.name}))
        print(f"Leído: {ruta.name} ({len(texto)} caracteres)")

    if not documentos:
        print("No se pudo extraer texto de ningún PDF.")
        return

    splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100)
    chunks = splitter.split_documents(documentos)
    if not chunks:
        print("No se generaron fragmentos para indexar.")
        return

    store = _store()
    store.reset_collection()  # reindexar no duplica fragmentos
    for i in range(0, len(chunks), 50):
        store.add_documents(chunks[i : i + 50])
        print(f"Indexados {min(i + 50, len(chunks))}/{len(chunks)} fragmentos...")

    print(f"Listo: {len(chunks)} fragmentos en la colección '{COLLECTION}'.")


if __name__ == "__main__":
    main()
