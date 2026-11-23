"""Lògica de negoci de Tasks_app, independent de la CLI i del disc."""

import re
from datetime import date

from models import ErrorTasques

MISSATGE_DATA_INVALIDA = "Error: format de data invàlid (YYYY-MM-DD)."
_PATRO_DATA = re.compile(r"[0-9]{4}-[0-9]{2}-[0-9]{2}")


def validar_data(text):
    """Valida una data en format YYYY-MM-DD i la retorna com a `date` (RF-06).

    Només s'accepta el format exacte YYYY-MM-DD (no variants ISO com
    `20261215`) i que sigui una data de calendari real.
    Llança `ErrorTasques` si la data no és vàlida.
    """
    if not _PATRO_DATA.fullmatch(text):
        raise ErrorTasques(MISSATGE_DATA_INVALIDA)
    try:
        return date.fromisoformat(text)
    except ValueError as error:
        raise ErrorTasques(MISSATGE_DATA_INVALIDA) from error
