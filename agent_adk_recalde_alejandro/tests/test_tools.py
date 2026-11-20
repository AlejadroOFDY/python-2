"""Validaciones de las herramientas. No requieren red ni Ollama.

Ejecutar desde la raíz del repo:
    python -m pytest tests -q
"""

from tools.tools import (
    _limitar,
    buscar_apuntes,
    buscar_en_internet,
    indexar_apunte,
)


def test_limitar_recorta_y_usa_defecto():
    assert _limitar(4, 4) == 4
    assert _limitar("9", 4) == 9
    assert _limitar(100, 4) == 10
    assert _limitar(0, 4) == 1
    assert _limitar("no-es-numero", 4) == 4
    assert _limitar(None, 5) == 5


def test_buscar_apuntes_rechaza_consulta_vacia():
    assert buscar_apuntes("").startswith("Error")
    assert buscar_apuntes("   ").startswith("Error")


def test_indexar_apunte_rechaza_texto_vacio_o_corto():
    assert indexar_apunte("").startswith("Error")
    assert indexar_apunte("corto").startswith("Error")


def test_buscar_en_internet_rechaza_consulta_vacia():
    assert buscar_en_internet("").startswith("Error")
    assert buscar_en_internet(None).startswith("Error")
