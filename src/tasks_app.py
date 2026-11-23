"""Tasks_app: eina CLI per gestionar tasques acadèmiques (RF-03, RF-04)."""

import argparse
import sys

from logica import validar_data
from models import ErrorTasques, Tasca
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

    subparsers.add_parser("list", help="mostra les tasques registrades")
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


def comandament_list(args):
    """Mostra totes les tasques registrades (RF-04)."""
    tasques = carregar_tasques()
    if not tasques:
        print("Registre de tasques buit.")
        return
    for tasca in tasques:
        print(
            f"[{tasca.id}] {tasca.titol} ({tasca.assignatura})"
            f" - estat: {tasca.estat}"
        )


COMANDAMENTS = {
    "add": comandament_add,
    "list": comandament_list,
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
