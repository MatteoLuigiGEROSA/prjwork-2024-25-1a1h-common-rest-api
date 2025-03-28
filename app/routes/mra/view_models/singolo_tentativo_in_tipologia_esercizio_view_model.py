import hashlib
import json

class SingoloTentativoInTipologiaEsercizioViewModel:
    """
    ViewModel per rappresentare un singolo tentativo in una tipologia di esercizio.
    """

    def __init__(self, id_tipologia, id_tentativo, dati_raw):
        self.id_tipologia = id_tipologia
        self.id_tentativo = id_tentativo
        self.pulsante = self._safe_get(dati_raw.get("sequenzaPulsanti", "").split(","), id_tentativo)
        self.tempo = self._safe_get(dati_raw.get("sequenzaTempo", "").split(","), id_tentativo)
        self.wait = self._safe_get(dati_raw.get("sequenzaWait", "").split(","), id_tentativo)

    def to_dict(self):
        core = {
            "id": str(self.id_tentativo),
            "pulsante-led": self.pulsante,
            "tempo-max-disponibile-ms": self.tempo,
            "intertempo-wait-ms": self.wait,
            "_links": {
                "self": f"/api/mra/v1.0.0/catalogo-tipologie-esercizi/{self.id_tipologia}/tentativi/{self.id_tentativo}",
                "catalogo_tipologia": f"/api/mra/v1.0.0/catalogo-tipologie-esercizi/{self.id_tipologia}"
            }
        }
        core["_hash"] = self._calcola_hash(core)
        return core

    def _safe_get(self, arr, i):
        try:
            return arr[i].strip()
        except IndexError:
            return None

    def _calcola_hash(self, core):
        subset = {k: core[k] for k in ["id", "pulsante-led", "tempo-max-disponibile-ms", "intertempo-wait-ms"]}
        json_ordinato = json.dumps(subset, sort_keys=True)
        return hashlib.sha256(json_ordinato.encode("utf-8")).hexdigest()
