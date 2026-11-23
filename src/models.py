"""Model de dades de Tasks_app (RF-01, RF-05, RNF-01)."""

from dataclasses import dataclass
from typing import Optional

ESTAT_PENDENT = "pendent"
ESTAT_COMPLETADA = "completada"


@dataclass
class Tasca:
    """Tasca acadèmica d'un estudiant.

    `data_limit` és opcional i s'emmagatzema en format YYYY-MM-DD.
    """

    id: int
    titol: str
    assignatura: str
    estat: str = ESTAT_PENDENT
    data_limit: Optional[str] = None

    def a_dict(self):
        """Serialitza la tasca a un diccionari compatible amb JSON.

        El camp `data_limit` només s'inclou si la tasca en té.
        """
        dades = {
            "id": self.id,
            "titol": self.titol,
            "assignatura": self.assignatura,
            "estat": self.estat,
        }
        if self.data_limit is not None:
            dades["data_limit"] = self.data_limit
        return dades

    @classmethod
    def des_de_dict(cls, dades):
        """Crea una tasca a partir d'un diccionari carregat de JSON.

        Accepta fitxers de la v1.0, sense el camp `data_limit` (RNF-01).
        """
        return cls(
            id=dades["id"],
            titol=dades["titol"],
            assignatura=dades["assignatura"],
            estat=dades.get("estat", ESTAT_PENDENT),
            data_limit=dades.get("data_limit"),
        )
