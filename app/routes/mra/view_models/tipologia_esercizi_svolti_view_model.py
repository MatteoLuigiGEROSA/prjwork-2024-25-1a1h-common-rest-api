import hashlib
import json

class TipologiaEserciziSvoltiViewModel:
    """
    ViewModel che rappresenta una tipologia di esercizio svolto da un atleta.
    Include metadati, hash e link HATEOAS.
    """

    def __init__(self, id_atleta, id_esercizio, sessioni_dict=None):
        self.id_atleta = id_atleta
        self.id_esercizio = id_esercizio
        self.sessioni_dict = sessioni_dict or {}

    def to_dict(self):
        sessioni_keys = list(self.sessioni_dict.keys()) if isinstance(self.sessioni_dict, dict) else []
        numero_sessioni = len(sessioni_keys)
        range_date = self._calcola_range_date(sessioni_keys)

        base_dict = {
            "id": self.id_esercizio,
            "numero_sessioni": numero_sessioni,
            "intervallo_date_sessioni": range_date
        }

        base_dict["_hash"] = self._calcola_hash(base_dict)

        base_dict["_links"] = {
            "self": f"/api/mra/v1.0.0/atleti/{self.id_atleta}/tipologie-esercizi-svolti/{self.id_esercizio}",
            "sessioni": f"/api/mra/v1.0.0/atleti/{self.id_atleta}/tipologie-esercizi-svolti/{self.id_esercizio}/sessioni"
        }

        return base_dict

    def _calcola_hash(self, entity_dict):
        chiavi = ["id", "numero_sessioni", "intervallo_date_sessioni"]
        dati_rilevanti = {k: entity_dict[k] for k in chiavi if k in entity_dict}
        json_ordinato = json.dumps(dati_rilevanti, sort_keys=True)
        return hashlib.sha256(json_ordinato.encode("utf-8")).hexdigest()

    def _calcola_range_date(self, sessioni_keys):
        try:
            timestamps = sorted(sessioni_keys)
            if len(timestamps) == 0:
                return None
            return {
                "prima_sessione": timestamps[0],
                "ultima_sessione": timestamps[-1]
            }
        except Exception:
            return None
