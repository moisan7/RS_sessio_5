"""Tests unitaris de la lògica de negoci (RF-06)."""

from datetime import date

import pytest

from logica import validar_data
from models import ErrorTasques

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
