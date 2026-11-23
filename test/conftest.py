"""Configuració i fixtures compartides pels tests de Tasks_app."""

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

ARREL = Path(__file__).resolve().parent.parent
SCRIPT = ARREL / "src" / "tasks_app.py"

sys.path.insert(0, str(ARREL / "src"))


@pytest.fixture
def executar(tmp_path):
    """Executa tasks_app com a subprocés dins d'una carpeta temporal.

    Així els tests mai modifiquen el `data/tasks.json` real.
    """

    def _executar(*args):
        entorn = dict(os.environ, PYTHONIOENCODING="utf-8")
        return subprocess.run(
            [sys.executable, str(SCRIPT), *args],
            cwd=tmp_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
            env=entorn,
        )

    return _executar


@pytest.fixture
def fitxer_dades(tmp_path):
    """Ruta del fitxer `data/tasks.json` dins de la carpeta temporal."""
    return tmp_path / "data" / "tasks.json"


@pytest.fixture
def sembrar_tasques(fitxer_dades):
    """Escriu una llista de tasques (diccionaris) a `data/tasks.json`."""

    def _sembrar(tasques):
        fitxer_dades.parent.mkdir(parents=True, exist_ok=True)
        fitxer_dades.write_text(
            json.dumps(tasques, ensure_ascii=False), encoding="utf-8"
        )

    return _sembrar
