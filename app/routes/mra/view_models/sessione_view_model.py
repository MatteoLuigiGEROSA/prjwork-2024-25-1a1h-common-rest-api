import hashlib
import json

class SessioneViewModel:
    """
    ViewModel per rappresentare una singola sessione svolta in una tipologia di esercizio.
    Include hash e link HATEOAS.
    """

    def __init__(self, id_atleta, id_esercizio, id_sessione, rilevazioni=None):
        self.id_atleta = id_atleta
        self.id_esercizio = id_esercizio
        self.id_sessione = id_sessione
        self.rilevazioni = rilevazioni or []

    def to_dict(self):
        base_dict = {
            "id": self.id_sessione,
            "numero_rilevazioni": len(self.rilevazioni)
        }

        base_dict["_hash"] = self._calcola_hash(base_dict)

        base_dict["_links"] = {
            "self": f"/api/mra/v1.0.0/atleti/{self.id_atleta}/tipologie-esercizi-svolti/{self.id_esercizio}/sessioni/{self.id_sessione}",
            "rilevazioni": f"/api/mra/v1.0.0/atleti/{self.id_atleta}/tipologie-esercizi-svolti/{self.id_esercizio}/sessioni/{self.id_sessione}/rilevazioni"
        }

        return base_dict

    def _calcola_hash(self, entity_dict):
        chiavi = ["id", "numero_rilevazioni"]
        dati = {k: entity_dict[k] for k in chiavi if k in entity_dict}
        json_ordinato = json.dumps(dati, sort_keys=True)
        return hashlib.sha256(json_ordinato.encode("utf-8")).hexdigest()
