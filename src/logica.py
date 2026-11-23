"""Lògica de negoci de Tasks_app, independent de la CLI i del disc."""

import re
from datetime import date

from models import ESTAT_COMPLETADA, ESTAT_PENDENT, ErrorTasques

MISSATGE_DATA_INVALIDA = "Error: format de data invàlid (YYYY-MM-DD)."
_PATRO_DATA = re.compile(r"[0-9]{4}-[0-9]{2}-[0-9]{2}")
INDICADOR_CADUCADA = "CADUCADA"
INDICADOR_URGENT = "URGENT"
DIES_URGENT = 7


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


def cercar_per_id(tasques, id_tasca):
    """Retorna la tasca amb l'ID indicat (RF-08).

    Llança `ErrorTasques` si no existeix cap tasca amb aquest ID.
    """
    for tasca in tasques:
        if tasca.id == id_tasca:
            return tasca
    raise ErrorTasques(f"Error: no existeix cap tasca amb ID {id_tasca}.")


def calcular_indicador(tasca, avui):
    """Retorna l'indicador d'una tasca segons la data actual (RF-13, RF-14).

    - `CADUCADA`: tasca pendent amb data límit anterior a `avui`.
    - `URGENT`: tasca pendent amb entre 0 i 6 dies fins a la data límit.
    - `None`: en qualsevol altre cas (tasca completada, sense data límit
      o amb la data límit a 7 dies o més).
    """
    if tasca.estat != ESTAT_PENDENT or tasca.data_limit is None:
        return None
    dies_restants = (date.fromisoformat(tasca.data_limit) - avui).days
    if dies_restants < 0:
        return INDICADOR_CADUCADA
    if dies_restants < DIES_URGENT:
        return INDICADOR_URGENT
    return None


def resum(tasques, avui):
    """Retorna el recompte de tasques del registre (RF-15, RF-16).

    El diccionari conserva l'ordre de presentació: Total, Pendents,
    Completades, Caducades i Urgents. Les caducades i les urgents són
    sempre tasques pendents (vegeu `calcular_indicador`).
    """
    indicadors = [calcular_indicador(tasca, avui) for tasca in tasques]
    return {
        "Total": len(tasques),
        "Pendents": sum(1 for t in tasques if t.estat == ESTAT_PENDENT),
        "Completades": sum(1 for t in tasques if t.estat == ESTAT_COMPLETADA),
        "Caducades": indicadors.count(INDICADOR_CADUCADA),
        "Urgents": indicadors.count(INDICADOR_URGENT),
    }


def filtrar_per_assignatura(tasques, assignatura):
    """Retorna les tasques de l'assignatura indicada (RF-17).

    La comparació és exacta però sense distingir majúscules de minúscules;
    els accents són significatius. Es conserva l'ordre original.
    """
    cercada = assignatura.casefold()
    return [t for t in tasques if t.assignatura.casefold() == cercada]


def filtrar_per_paraula(tasques, paraula):
    """Retorna les tasques que contenen la paraula al títol (RF-18).

    La cerca és per subcadena, en qualsevol posició del títol, sense
    distingir majúscules de minúscules; els accents són significatius.
    """
    cercada = paraula.casefold()
    return [t for t in tasques if cercada in t.titol.casefold()]


def filtrar_tasques(tasques, assignatura=None, paraula=None):
    """Aplica els filtres indicats; si n'hi ha dos, han de complir-se tots
    dos (RF-17, RF-18, RF-19).

    Un filtre amb valor `None` no s'aplica.
    """
    if assignatura is not None:
        tasques = filtrar_per_assignatura(tasques, assignatura)
    if paraula is not None:
        tasques = filtrar_per_paraula(tasques, paraula)
    return list(tasques)
