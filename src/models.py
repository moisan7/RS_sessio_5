"""Model de dades de Tasks_app (RF-01)."""

from dataclasses import dataclass

ESTAT_PENDENT = "pendent"


@dataclass
class Tasca:
    """Tasca acadèmica d'un estudiant."""

    id: int
    titol: str
    assignatura: str
    estat: str = ESTAT_PENDENT

    def a_dict(self):
        """Serialitza la tasca a un diccionari compatible amb JSON."""
        return {
            "id": self.id,
            "titol": self.titol,
            "assignatura": self.assignatura,
            "estat": self.estat,
        }

    @classmethod
    def des_de_dict(cls, dades):
        """Crea una tasca a partir d'un diccionari carregat de JSON."""
        return cls(
            id=dades["id"],
            titol=dades["titol"],
            assignatura=dades["assignatura"],
            estat=dades.get("estat", ESTAT_PENDENT),
        )
