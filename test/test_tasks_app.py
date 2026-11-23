"""Tests d'integració de Tasks_app: escenaris GS-01, GS-02 i GS-03."""

import json

import pytest


def test_gs_01_creacio_correcta_d_una_tasca(executar, fitxer_dades):
    """GS-01 (RF-01, RF-03): afegir una tasca a una base de dades buida."""
    resultat = executar("add", "--title", "Pràctica 1", "--subject", "RS")

    assert resultat.returncode == 0
    assert "Tasca [ID: 1] creada amb èxit" in resultat.stdout
    tasques = json.loads(fitxer_dades.read_text(encoding="utf-8"))
    assert tasques == [
        {
            "id": 1,
            "titol": "Pràctica 1",
            "assignatura": "RS",
            "estat": "pendent",
        }
    ]


def test_gs_02_llistat_sense_registres(executar, fitxer_dades):
    """GS-02 (RF-02, RF-04): llistar quan no hi ha tasques."""
    resultat = executar("list")

    assert resultat.returncode == 0
    assert "Registre de tasques buit." in resultat.stdout
    assert json.loads(fitxer_dades.read_text(encoding="utf-8")) == []


def test_gs_03_llistat_amb_registres(executar, sembrar_tasques):
    """GS-03 (RF-04): llistar quan hi ha tasques registrades."""
    sembrar_tasques(
        [
            {
                "id": 1,
                "titol": "Pràctica 1",
                "assignatura": "RS",
                "estat": "pendent",
            },
            {
                "id": 2,
                "titol": "Examen parcial",
                "assignatura": "SO",
                "estat": "pendent",
            },
        ]
    )

    resultat = executar("list")

    assert resultat.returncode == 0
    assert resultat.stdout.splitlines() == [
        "[1] Pràctica 1 (RS) - estat: pendent",
        "[2] Examen parcial (SO) - estat: pendent",
    ]


@pytest.mark.parametrize(
    "contingut",
    ["{no es json", '{"id": 1}', '[{"id": 1}]'],
    ids=["json_mal_format", "no_es_llista", "falten_camps"],
)
def test_gs_17_fitxer_de_dades_amb_contingut_invalid(
    executar, fitxer_dades, contingut
):
    """GS-17 (RNF-05, RNF-03): contingut invàlid, error i fitxer intacte."""
    fitxer_dades.parent.mkdir(parents=True, exist_ok=True)
    fitxer_dades.write_text(contingut, encoding="utf-8")

    for comandament in (
        ["list"],
        ["add", "--title", "X", "--subject", "RS"],
    ):
        resultat = executar(*comandament)

        assert resultat.returncode == 1
        assert resultat.stdout == ""
        assert (
            "Error: el fitxer data/tasks.json no conté JSON vàlid."
            in resultat.stderr
        )
        assert fitxer_dades.read_text(encoding="utf-8") == contingut


def test_gs_04_creacio_d_una_tasca_amb_data_limit(executar, fitxer_dades):
    """GS-04 (RF-05): afegir una tasca amb data límit."""
    resultat = executar(
        "add", "--title", "Pràctica 2", "--subject", "RS",
        "--due", "2026-12-15",
    )

    assert resultat.returncode == 0
    assert "Tasca [ID: 1] creada amb èxit" in resultat.stdout
    tasques = json.loads(fitxer_dades.read_text(encoding="utf-8"))
    assert tasques == [
        {
            "id": 1,
            "titol": "Pràctica 2",
            "assignatura": "RS",
            "estat": "pendent",
            "data_limit": "2026-12-15",
        }
    ]


@pytest.mark.parametrize(
    "data",
    ["15/12/2026", "2026-13-01", "2026-02-30", "demà"],
    ids=["format", "mes", "dia", "text"],
)
def test_gs_05_rebuig_d_una_data_limit_invalida(
    executar, fitxer_dades, data
):
    """GS-05 (RF-06, RNF-03): una data invàlida es rebutja sense desar."""
    resultat = executar(
        "add", "--title", "Pràctica 2", "--subject", "RS", "--due", data
    )

    assert resultat.returncode == 1
    assert resultat.stdout == ""
    assert "Error: format de data invàlid (YYYY-MM-DD)." in resultat.stderr
    assert json.loads(fitxer_dades.read_text(encoding="utf-8")) == []
