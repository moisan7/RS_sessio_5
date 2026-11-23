"""Tests unitaris del model Tasca (RNF-01, RF-05)."""

from models import Tasca


def test_rnf_01_carrega_tasca_de_la_v1_sense_data_limit():
    """RNF-01: una tasca sense `data_limit` es carrega sense data."""
    dades_v1 = {
        "id": 1,
        "titol": "Pràctica 1",
        "assignatura": "RS",
        "estat": "pendent",
    }

    tasca = Tasca.des_de_dict(dades_v1)

    assert tasca.data_limit is None
    assert tasca.estat == "pendent"


def test_rf_05_serialitzacio_amb_data_limit():
    """RF-05: la data límit es desa i es recupera sense pèrdues."""
    tasca = Tasca(1, "Pràctica 2", "RS", "pendent", "2026-12-15")

    dades = tasca.a_dict()

    assert dades["data_limit"] == "2026-12-15"
    assert Tasca.des_de_dict(dades) == tasca


def test_rnf_01_serialitzacio_sense_data_limit_no_afegeix_el_camp():
    """RNF-01: una tasca sense data límit es desa com a la v1.0."""
    tasca = Tasca(1, "Pràctica 1", "RS")

    assert tasca.a_dict() == {
        "id": 1,
        "titol": "Pràctica 1",
        "assignatura": "RS",
        "estat": "pendent",
    }
