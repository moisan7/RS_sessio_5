"""Persistència de les tasques en un fitxer JSON local (RF-01, RF-02)."""

import json
from pathlib import Path

from models import Tasca

RUTA_PER_DEFECTE = Path("data") / "tasks.json"


def desar_tasques(tasques, ruta=RUTA_PER_DEFECTE):
    """Desa la llista de tasques al fitxer JSON (RF-01)."""
    ruta = Path(ruta)
    ruta.parent.mkdir(parents=True, exist_ok=True)
    dades = [tasca.a_dict() for tasca in tasques]
    with open(ruta, "w", encoding="utf-8") as fitxer:
        json.dump(dades, fitxer, ensure_ascii=False, indent=2)
        fitxer.write("\n")


def carregar_tasques(ruta=RUTA_PER_DEFECTE):
    """Carrega les tasques del fitxer JSON.

    Si el fitxer no existeix, el crea amb una llista buida (RF-02).
    """
    ruta = Path(ruta)
    if not ruta.exists():
        desar_tasques([], ruta)
        return []
    with open(ruta, encoding="utf-8") as fitxer:
        dades = json.load(fitxer)
    return [Tasca.des_de_dict(element) for element in dades]
