"""Tests d'integració de Tasks_app: escenaris Gherkin de la v1.0 i v2.0."""

import json
from datetime import date, timedelta

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


def _tasca(id_tasca=1, titol="Pràctica 1", assignatura="RS", **extra):
    """Diccionari d'una tasca pendent per sembrar `data/tasks.json`."""
    return {
        "id": id_tasca,
        "titol": titol,
        "assignatura": assignatura,
        "estat": "pendent",
        **extra,
    }


def _llegir(fitxer_dades):
    return json.loads(fitxer_dades.read_text(encoding="utf-8"))


def test_gs_06_modificacio_del_titol_i_de_l_assignatura(
    executar, fitxer_dades, sembrar_tasques
):
    """GS-06 (RF-07): es modifiquen només els atributs indicats."""
    sembrar_tasques([_tasca(titol="Practica 1"), _tasca(2, "Examen", "SO")])

    resultat = executar(
        "edit", "--id", "1", "--title", "Pràctica 1", "--subject", "SO"
    )

    assert resultat.returncode == 0
    assert "Tasca [ID: 1] modificada amb èxit" in resultat.stdout
    assert _llegir(fitxer_dades) == [
        _tasca(titol="Pràctica 1", assignatura="SO"),
        _tasca(2, "Examen", "SO"),
    ]


def test_gs_07_modificacio_de_la_data_limit_i_de_l_estat(
    executar, fitxer_dades, sembrar_tasques
):
    """GS-07 (RF-07): es poden modificar la data límit i l'estat."""
    sembrar_tasques([_tasca()])

    resultat = executar(
        "edit", "--id", "1", "--due", "2026-12-20", "--status", "completada"
    )

    assert resultat.returncode == 0
    assert "Tasca [ID: 1] modificada amb èxit" in resultat.stdout
    assert _llegir(fitxer_dades) == [
        {**_tasca(), "estat": "completada", "data_limit": "2026-12-20"}
    ]


def test_gs_08_edit_amb_identificador_inexistent(
    executar, fitxer_dades, sembrar_tasques
):
    """GS-08 (RF-08, RNF-03): edit d'un ID inexistent no canvia res."""
    sembrar_tasques([_tasca()])
    abans = fitxer_dades.read_bytes()

    resultat = executar("edit", "--id", "99", "--title", "Nou")

    assert resultat.returncode == 1
    assert resultat.stdout == ""
    assert "Error: no existeix cap tasca amb ID 99." in resultat.stderr
    assert fitxer_dades.read_bytes() == abans


def test_gs_09_edicio_sense_cap_atribut(
    executar, fitxer_dades, sembrar_tasques
):
    """GS-09 (RF-09, RNF-03): edit sense atributs és un error."""
    sembrar_tasques([_tasca()])
    abans = fitxer_dades.read_bytes()

    resultat = executar("edit", "--id", "1")

    assert resultat.returncode == 1
    assert resultat.stdout == ""
    assert (
        "Error: cal indicar almenys un atribut a modificar."
        in resultat.stderr
    )
    assert fitxer_dades.read_bytes() == abans


def test_rf_06_edit_amb_data_limit_invalida_no_canvia_res(
    executar, fitxer_dades, sembrar_tasques
):
    """RF-06: una data invàlida a edit es rebutja sense canvis parcials."""
    sembrar_tasques([_tasca()])
    abans = fitxer_dades.read_bytes()

    resultat = executar(
        "edit", "--id", "1", "--title", "Nou", "--due", "15/12/2026"
    )

    assert resultat.returncode == 1
    assert "Error: format de data invàlid (YYYY-MM-DD)." in resultat.stderr
    assert fitxer_dades.read_bytes() == abans


def test_rf_07_edit_amb_estat_desconegut_es_rebutja(
    executar, fitxer_dades, sembrar_tasques
):
    """RF-07: només s'accepten els estats `pendent` i `completada`."""
    sembrar_tasques([_tasca()])
    abans = fitxer_dades.read_bytes()

    resultat = executar("edit", "--id", "1", "--status", "oblidada")

    assert resultat.returncode != 0
    assert fitxer_dades.read_bytes() == abans


def test_gs_08_complete_amb_identificador_inexistent(
    executar, fitxer_dades, sembrar_tasques
):
    """GS-08 (RF-08, RNF-03): complete d'un ID inexistent no canvia res."""
    sembrar_tasques([_tasca()])
    abans = fitxer_dades.read_bytes()

    resultat = executar("complete", "--id", "99")

    assert resultat.returncode == 1
    assert resultat.stdout == ""
    assert "Error: no existeix cap tasca amb ID 99." in resultat.stderr
    assert fitxer_dades.read_bytes() == abans


def test_gs_10_completar_una_tasca_pendent(
    executar, fitxer_dades, sembrar_tasques
):
    """GS-10 (RF-10): la tasca passa a l'estat `completada`."""
    sembrar_tasques([_tasca(), _tasca(2, "Examen", "SO")])

    resultat = executar("complete", "--id", "1")

    assert resultat.returncode == 0
    assert "Tasca [ID: 1] marcada com a completada" in resultat.stdout
    assert _llegir(fitxer_dades) == [
        {**_tasca(), "estat": "completada"},
        _tasca(2, "Examen", "SO"),
    ]


def test_gs_11_completar_una_tasca_ja_completada(
    executar, fitxer_dades, sembrar_tasques
):
    """GS-11 (RF-11): es informa i el fitxer no canvia."""
    sembrar_tasques([{**_tasca(), "estat": "completada"}])
    abans = fitxer_dades.read_bytes()

    resultat = executar("complete", "--id", "1")

    assert resultat.returncode == 0
    assert "La tasca [ID: 1] ja estava completada." in resultat.stdout
    assert fitxer_dades.read_bytes() == abans


def test_rf_10_complete_conserva_la_data_limit(
    executar, fitxer_dades, sembrar_tasques
):
    """RF-10: completar no esborra els altres atributs de la tasca."""
    sembrar_tasques([_tasca(data_limit="2026-12-15")])

    executar("complete", "--id", "1")

    assert _llegir(fitxer_dades) == [
        {**_tasca(), "estat": "completada", "data_limit": "2026-12-15"}
    ]


def _data_relativa(dies):
    """Data ISO a `dies` dies de la data actual (negatiu: passat)."""
    return (date.today() + timedelta(days=dies)).isoformat()


def test_gs_12_llistat_d_una_tasca_amb_data_limit_llunyana(
    executar, sembrar_tasques
):
    """GS-12 (RF-12): es mostra la data límit i cap indicador."""
    limit = _data_relativa(30)
    sembrar_tasques([_tasca(1, "Pràctica 2", "RS", data_limit=limit)])

    resultat = executar("list")

    assert resultat.returncode == 0
    assert resultat.stdout.splitlines() == [
        f"[1] Pràctica 2 (RS) - estat: pendent - límit: {limit}"
    ]


def test_gs_13_llistat_d_una_tasca_pendent_caducada(
    executar, sembrar_tasques
):
    """GS-13 (RF-13): una tasca pendent vençuda ahir és CADUCADA."""
    limit = _data_relativa(-1)
    sembrar_tasques([_tasca(1, "Examen parcial", "SO", data_limit=limit)])

    resultat = executar("list")

    assert resultat.returncode == 0
    assert resultat.stdout.splitlines() == [
        f"[1] Examen parcial (SO) - estat: pendent - límit: {limit}"
        " [CADUCADA]"
    ]


def test_rf_12_el_llistat_barreja_tasques_amb_i_sense_data_limit(
    executar, sembrar_tasques
):
    """RF-12: les tasques sense data conserven el format de la v1.0."""
    limit = _data_relativa(2)
    sembrar_tasques(
        [_tasca(1), _tasca(2, "Examen", "SO", data_limit=limit)]
    )

    resultat = executar("list")

    assert resultat.stdout.splitlines() == [
        "[1] Pràctica 1 (RS) - estat: pendent",
        f"[2] Examen (SO) - estat: pendent - límit: {limit} [URGENT]",
    ]


@pytest.mark.parametrize(
    "dies, indicador",
    [(0, " [URGENT]"), (6, " [URGENT]"), (7, "")],
    ids=["avui", "d_aqui_6_dies", "d_aqui_7_dies"],
)
def test_gs_14_indicador_segons_els_dies_que_falten(
    executar, sembrar_tasques, dies, indicador
):
    """GS-14 (RF-14): 0 i 6 dies són URGENT, 7 dies ja no."""
    limit = _data_relativa(dies)
    sembrar_tasques([_tasca(data_limit=limit)])

    resultat = executar("list")

    assert resultat.returncode == 0
    assert resultat.stdout.splitlines() == [
        f"[1] Pràctica 1 (RS) - estat: pendent - límit: {limit}{indicador}"
    ]


@pytest.mark.parametrize(
    "dies", [-30, -1, 0, 3], ids=["molt_passada", "ahir", "avui", "d_aqui_3"]
)
def test_gs_15_una_tasca_completada_no_es_marca_mai(
    executar, sembrar_tasques, dies
):
    """GS-15 (RF-13, RF-14): una tasca completada no té indicador."""
    limit = _data_relativa(dies)
    sembrar_tasques([{**_tasca(data_limit=limit), "estat": "completada"}])

    resultat = executar("list")

    assert resultat.returncode == 0
    assert resultat.stdout.splitlines() == [
        f"[1] Pràctica 1 (RS) - estat: completada - límit: {limit}"
    ]


def test_gs_16_compatibilitat_amb_el_fitxer_de_la_v1(
    executar, sembrar_tasques
):
    """GS-16 (RNF-01): una tasca sense `data_limit` es llista com a la v1."""
    sembrar_tasques([_tasca()])

    resultat = executar("list")

    assert resultat.returncode == 0
    assert resultat.stdout.splitlines() == [
        "[1] Pràctica 1 (RS) - estat: pendent"
    ]
