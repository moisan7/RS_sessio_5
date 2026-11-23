"""Tests d'integració de Tasks_app: escenaris GS-01, GS-02 i GS-03."""

import json


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


def test_gs_17_fitxer_de_dades_amb_json_invalid(
    executar, fitxer_dades
):
    """GS-17 (RNF-05, RNF-03): JSON invàlid, error i fitxer intacte."""
    fitxer_dades.parent.mkdir(parents=True, exist_ok=True)
    fitxer_dades.write_text("{no es json", encoding="utf-8")

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
        assert fitxer_dades.read_text(encoding="utf-8") == "{no es json"
