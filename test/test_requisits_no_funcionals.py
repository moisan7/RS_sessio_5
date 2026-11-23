"""Tests dels requisits no funcionals RNF-02 i RNF-04."""

import ast
import re
import sys
from pathlib import Path

ARREL = Path(__file__).resolve().parent.parent
CARPETA_SRC = ARREL / "src"


def _moduls_importats(fitxer):
    """Noms dels mòduls de primer nivell que importa un fitxer."""
    arbre = ast.parse(fitxer.read_text(encoding="utf-8"))
    noms = set()
    for node in ast.walk(arbre):
        if isinstance(node, ast.Import):
            noms.update(alies.name.split(".")[0] for alies in node.names)
        elif isinstance(node, ast.ImportFrom) and node.level == 0:
            noms.add(node.module.split(".")[0])
    return noms


def test_rnf_02_el_codi_font_nomes_usa_la_biblioteca_estandard():
    """RNF-02: `src/` només importa la biblioteca estàndard i mòduls propis."""
    propis = {fitxer.stem for fitxer in CARPETA_SRC.glob("*.py")}
    permesos = set(sys.stdlib_module_names) | propis

    for fitxer in CARPETA_SRC.glob("*.py"):
        externs = _moduls_importats(fitxer) - permesos
        assert not externs, f"{fitxer.name} importa {sorted(externs)}"


def test_rnf_04_el_fitxer_de_dades_es_desa_en_utf8_i_amb_dates_iso(
    executar, fitxer_dades
):
    """RNF-04: accents sense escapar (UTF-8) i data límit YYYY-MM-DD."""
    executar(
        "add", "--title", "Pràctica d'ampliació", "--subject", "Química",
        "--due", "2026-12-15",
    )

    text = fitxer_dades.read_bytes().decode("utf-8")

    assert "Pràctica d'ampliació" in text
    assert "Química" in text
    assert "\\u" not in text
    assert re.search(r'"data_limit": "\d{4}-\d{2}-\d{2}"', text)
