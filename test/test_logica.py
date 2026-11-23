"""Tests unitaris de la lògica de negoci (RF-06, RF-08, RF-13, RF-14)."""

from datetime import date

import pytest

from logica import calcular_indicador, cercar_per_id, validar_data
from models import ErrorTasques, Tasca

MISSATGE = "Error: format de data invàlid (YYYY-MM-DD)."


def test_rf_06_data_valida_es_retorna_com_a_date():
    """RF-06: una data YYYY-MM-DD correcta s'accepta."""
    assert validar_data("2026-12-15") == date(2026, 12, 15)


def test_rf_06_accepta_el_29_de_febrer_d_un_any_de_traspas():
    """RF-06: el 29 de febrer és vàlid només en anys de traspàs."""
    assert validar_data("2028-02-29") == date(2028, 2, 29)
    with pytest.raises(ErrorTasques):
        validar_data("2027-02-29")


@pytest.mark.parametrize(
    "text",
    [
        "15/12/2026",
        "2026-13-01",
        "2026-02-30",
        "2026-12-32",
        "demà",
        "",
        "2026-1-5",
        "20261215",
        "2026-W50-1",
        " 2026-12-15",
        "2026-12-15\n",
        "٢٠٢٦-١٢-١٥",
    ],
)
def test_rf_06_data_invalida_llanca_error(text):
    """RF-06: formats incorrectes o dates inexistents es rebutgen."""
    with pytest.raises(ErrorTasques) as excepcio:
        validar_data(text)

    assert str(excepcio.value) == MISSATGE


def test_rf_08_cerca_una_tasca_existent_per_id():
    """RF-08: es retorna la tasca que té l'ID indicat."""
    tasques = [Tasca(1, "Pràctica 1", "RS"), Tasca(5, "Examen", "SO")]

    assert cercar_per_id(tasques, 5) is tasques[1]


@pytest.mark.parametrize("id_tasca", [99, 0, -1])
def test_rf_08_id_inexistent_llanca_error(id_tasca):
    """RF-08: un ID sense tasca provoca l'error amb l'ID demanat."""
    tasques = [Tasca(1, "Pràctica 1", "RS")]

    with pytest.raises(ErrorTasques) as excepcio:
        cercar_per_id(tasques, id_tasca)

    assert str(excepcio.value) == (
        f"Error: no existeix cap tasca amb ID {id_tasca}."
    )


def test_rf_08_llista_buida_llanca_error():
    """RF-08: en un registre buit cap ID existeix."""
    with pytest.raises(ErrorTasques):
        cercar_per_id([], 1)


AVUI = date(2026, 11, 23)


def _pendent(data_limit):
    return Tasca(1, "Pràctica 1", "RS", "pendent", data_limit)


@pytest.mark.parametrize(
    "data_limit, esperat",
    [
        ("2026-01-01", "CADUCADA"),
        ("2026-11-21", "CADUCADA"),
        ("2026-11-22", "CADUCADA"),
        ("2026-11-23", "URGENT"),
        ("2026-11-24", "URGENT"),
        ("2026-11-29", "URGENT"),
        ("2026-11-30", None),
        ("2026-12-15", None),
        ("2027-11-23", None),
    ],
    ids=[
        "fa_mesos", "fa_2_dies", "ahir", "avui", "dema", "d_aqui_6_dies",
        "d_aqui_7_dies", "d_aqui_3_setmanes", "d_aqui_1_any",
    ],
)
def test_gs_13_gs_14_indicador_d_una_tasca_pendent(data_limit, esperat):
    """GS-13, GS-14 (RF-13, RF-14): límits de caducada i urgent."""
    assert calcular_indicador(_pendent(data_limit), AVUI) == esperat


@pytest.mark.parametrize(
    "data_limit", ["2026-11-01", "2026-11-23", "2026-11-25"]
)
def test_gs_15_una_tasca_completada_no_es_marca_mai(data_limit):
    """GS-15 (RF-13, RF-14): completada, sense indicador."""
    tasca = Tasca(1, "Pràctica 1", "RS", "completada", data_limit)

    assert calcular_indicador(tasca, AVUI) is None


def test_rnf_01_una_tasca_sense_data_limit_no_es_marca_mai():
    """RNF-01: sense data límit no hi ha indicador."""
    assert calcular_indicador(_pendent(None), AVUI) is None


def test_rf_14_el_canvi_de_dia_canvia_l_indicador():
    """RF-14: la mateixa tasca passa de urgent a caducada l'endemà."""
    tasca = _pendent("2026-11-23")

    assert calcular_indicador(tasca, date(2026, 11, 23)) == "URGENT"
    assert calcular_indicador(tasca, date(2026, 11, 24)) == "CADUCADA"
