import hashlib
import json

class TipologiaEsercizioViewModel:
    """
    ViewModel per una singola tipologia di esercizio dal catalogo.
    Trasforma i dati grezzi in formato RESTful con HATEOAS e hash.
    """

    def __init__(self, id_tipologia, dati_raw):
        self.id = str(id_tipologia)
        self.nome = dati_raw.get("nomeEsercizio")

        sequenza = dati_raw.get("sequenza", {})
        self.numero_tentativi = int(sequenza.get("totalePulsanti", 0))

    def to_dict(self):
        base_dict = {
            "id": self.id,
            "nome": self.nome,
            "numero_tentativi": self.numero_tentativi
        }

        base_dict["_hash"] = self._calcola_hash(base_dict)

        base_dict["_links"] = {
            "self": f"/api/mra/v1.0.0/catalogo-tipologie-esercizi/{self.id}",
            "tentativi": f"/api/mra/v1.0.0/catalogo-tipologie-esercizi/{self.id}/tentativi"
        }

        return base_dict

    def _calcola_hash(self, base_dict):
        core_fields = {k: base_dict[k] for k in ["id", "nome", "numero_tentativi"]}
        json_ordinato = json.dumps(core_fields, sort_keys=True)
        return hashlib.sha256(json_ordinato.encode("utf-8")).hexdigest()
