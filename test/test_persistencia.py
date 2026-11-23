"""Tests unitaris de la persistència (RF-01, RF-02, RNF-05)."""

import pytest

from models import ErrorTasques, Tasca
from persistencia import carregar_tasques, desar_tasques


def test_rf_02_crea_el_fitxer_buit_si_no_existeix(tmp_path):
    """RF-02: si no existeix, es crea amb una llista buida."""
    ruta = tmp_path / "data" / "tasks.json"

    assert carregar_tasques(ruta) == []
    assert ruta.read_text(encoding="utf-8").strip() == "[]"


def test_rf_01_desa_i_carrega_tasques(tmp_path):
    """RF-01: les tasques desades es recuperen iguals."""
    ruta = tmp_path / "tasks.json"
    tasques = [Tasca(1, "Pràctica 1", "RS"), Tasca(2, "Examen", "SO")]

    desar_tasques(tasques, ruta)

    assert carregar_tasques(ruta) == tasques


@pytest.mark.parametrize(
    "contingut",
    ["{no es json", '{"id": 1}', '[{"id": 1}]'],
    ids=["json_mal_format", "no_es_llista", "falten_camps"],
)
def test_rnf_05_json_invalid_llanca_error_sense_sobreescriure(
    tmp_path, contingut
):
    """RNF-05: un fitxer invàlid provoca un error i no es modifica."""
    ruta = tmp_path / "tasks.json"
    ruta.write_text(contingut, encoding="utf-8")

    with pytest.raises(ErrorTasques) as excepcio:
        carregar_tasques(ruta)

    assert str(excepcio.value) == (
        "Error: el fitxer data/tasks.json no conté JSON vàlid."
    )
    assert ruta.read_text(encoding="utf-8") == contingut
