"""Tasks_app: eina CLI per gestionar tasques acadèmiques (RF-03..RF-14)."""

import argparse
import sys
from datetime import date

from logica import (
    calcular_indicador,
    cercar_per_id,
    filtrar_tasques,
    resum,
    validar_data,
)
from models import ESTAT_COMPLETADA, ESTAT_PENDENT, ErrorTasques, Tasca
from persistencia import carregar_tasques, desar_tasques


def crear_parser():
    """Construeix el parser d'arguments amb els comandaments disponibles."""
    parser = argparse.ArgumentParser(
        prog="tasks_app",
        description="Gestor de tasques acadèmiques.",
    )
    subparsers = parser.add_subparsers(dest="comandament", required=True)

    parser_add = subparsers.add_parser("add", help="afegeix una tasca")
    parser_add.add_argument("--title", required=True, help="títol de la tasca")
    parser_add.add_argument(
        "--subject", required=True, help="assignatura de la tasca"
    )
    parser_add.add_argument(
        "--due", help="data límit de la tasca (format YYYY-MM-DD)"
    )

    parser_edit = subparsers.add_parser("edit", help="modifica una tasca")
    parser_edit.add_argument(
        "--id", type=int, required=True, help="ID de la tasca a modificar"
    )
    parser_edit.add_argument("--title", help="nou títol")
    parser_edit.add_argument("--subject", help="nova assignatura")
    parser_edit.add_argument(
        "--due", help="nova data límit (format YYYY-MM-DD)"
    )
    parser_edit.add_argument(
        "--status",
        choices=[ESTAT_PENDENT, ESTAT_COMPLETADA],
        help="nou estat",
    )

    parser_complete = subparsers.add_parser(
        "complete", help="marca una tasca com a completada"
    )
    parser_complete.add_argument(
        "--id", type=int, required=True, help="ID de la tasca a completar"
    )

    parser_list = subparsers.add_parser(
        "list", help="mostra les tasques registrades"
    )
    parser_list.add_argument(
        "--subject", help="mostra només les tasques d'aquesta assignatura"
    )
    parser_list.add_argument(
        "--keyword",
        help="mostra només les tasques amb aquesta paraula al títol",
    )
    subparsers.add_parser("summary", help="mostra un resum del registre")
    return parser


def comandament_add(args):
    """Crea una nova tasca amb estat 'pendent' (RF-03, RF-05, RF-06)."""
    tasques = carregar_tasques()
    data_limit = None
    if args.due is not None:
        data_limit = validar_data(args.due).isoformat()
    nou_id = max((tasca.id for tasca in tasques), default=0) + 1
    tasques.append(
        Tasca(nou_id, args.title, args.subject, data_limit=data_limit)
    )
    desar_tasques(tasques)
    print(f"Tasca [ID: {nou_id}] creada amb èxit")


def comandament_edit(args):
    """Modifica atributs d'una tasca a partir del seu ID (RF-07..RF-09).

    Totes les validacions es fan abans de modificar res, de manera que
    un error no altera mai `data/tasks.json`.
    """
    canvis = {
        "titol": args.title,
        "assignatura": args.subject,
        "data_limit": args.due,
        "estat": args.status,
    }
    if all(valor is None for valor in canvis.values()):
        raise ErrorTasques(
            "Error: cal indicar almenys un atribut a modificar."
        )
    tasques = carregar_tasques()
    tasca = cercar_per_id(tasques, args.id)
    if args.due is not None:
        canvis["data_limit"] = validar_data(args.due).isoformat()
    for atribut, valor in canvis.items():
        if valor is not None:
            setattr(tasca, atribut, valor)
    desar_tasques(tasques)
    print(f"Tasca [ID: {tasca.id}] modificada amb èxit")


def comandament_complete(args):
    """Marca una tasca com a completada (RF-10, RF-11, RF-08)."""
    tasques = carregar_tasques()
    tasca = cercar_per_id(tasques, args.id)
    if tasca.estat == ESTAT_COMPLETADA:
        print(f"La tasca [ID: {tasca.id}] ja estava completada.")
        return
    tasca.estat = ESTAT_COMPLETADA
    desar_tasques(tasques)
    print(f"Tasca [ID: {tasca.id}] marcada com a completada")


def comandament_list(args):
    """Mostra les tasques registrades (RF-04, RF-12..RF-14, RF-17..RF-20)."""
    tasques = carregar_tasques()
    if not tasques:
        print("Registre de tasques buit.")
        return
    seleccionades = filtrar_tasques(tasques, args.subject, args.keyword)
    if not seleccionades:
        print("Cap tasca coincideix amb els filtres.")
        return
    avui = date.today()
    for tasca in seleccionades:
        print(formatar_tasca(tasca, avui))


def comandament_summary(args):
    """Mostra el resum del registre de tasques (RF-15, RF-16)."""
    tasques = carregar_tasques()
    for nom, quantitat in resum(tasques, date.today()).items():
        print(f"{nom}: {quantitat}")


def formatar_tasca(tasca, avui):
    """Retorna la línia de llistat d'una tasca (RF-12, RF-13, RF-14)."""
    linia = (
        f"[{tasca.id}] {tasca.titol} ({tasca.assignatura})"
        f" - estat: {tasca.estat}"
    )
    if tasca.data_limit is not None:
        linia += f" - límit: {tasca.data_limit}"
    indicador = calcular_indicador(tasca, avui)
    if indicador is not None:
        linia += f" [{indicador}]"
    return linia


COMANDAMENTS = {
    "add": comandament_add,
    "edit": comandament_edit,
    "complete": comandament_complete,
    "list": comandament_list,
    "summary": comandament_summary,
}


def main(argv=None):
    """Punt d'entrada de l'aplicació."""
    for sortida in (sys.stdout, sys.stderr):
        if hasattr(sortida, "reconfigure"):
            sortida.reconfigure(encoding="utf-8")
    args = crear_parser().parse_args(argv)
    try:
        COMANDAMENTS[args.comandament](args)
    except ErrorTasques as error:
        print(error, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
