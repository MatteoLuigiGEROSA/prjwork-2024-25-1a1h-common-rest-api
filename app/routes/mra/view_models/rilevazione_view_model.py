import hashlib
import json

class RilevazioneViewModel:
    """
    ViewModel per rappresentare una singola rilevazione decodificata.
    Include hash, HATEOAS e semantica separata per le 3 componenti di "valore".
    """

    def __init__(self, id_atleta, id_esercizio, id_sessione, id_rilevazione, valore_raw):
        self.id_atleta = id_atleta
        self.id_esercizio = id_esercizio
        self.id_sessione = id_sessione
        self.id_rilevazione = id_rilevazione

        self.pulsante_proposto = None
        self.pulsante_premuto = None
        self.tempo_risposta_ms = None

        self._decodifica_valore(valore_raw)

    def to_dict(self):
        data = {
            "id": self.id_rilevazione,
            "pulsante_proposto": self.pulsante_proposto,
            "pulsante_premuto": self.pulsante_premuto,
            "tempo_risposta_ms": self.tempo_risposta_ms
        }

        data["_hash"] = self._calcola_hash(data)
        data["_links"] = {
            "self": f"/api/mra/v1.0.0/atleti/{self.id_atleta}/tipologie-esercizi-svolti/{self.id_esercizio}/sessioni/{self.id_sessione}/rilevazioni/{self.id_rilevazione}",
            "sessione": f"/api/mra/v1.0.0/atleti/{self.id_atleta}/tipologie-esercizi-svolti/{self.id_esercizio}/sessioni/{self.id_sessione}",
            "tipologia_esercizi_svolti": f"/api/mra/v1.0.0/atleti/{self.id_atleta}/tipologie-esercizi-svolti/{self.id_esercizio}",
            "atleta": f"/api/mra/v1.0.0/atleti/{self.id_atleta}"
        }

        return data

    def _decodifica_valore(self, valore):
        try:
            parti = valore.split(",")
            if len(parti) == 3:
                self.pulsante_proposto = int(parti[0])
                self.pulsante_premuto = int(parti[1])
                self.tempo_risposta_ms = int(parti[2])
        except Exception:
            pass  # In caso di errore lasceremo i valori a None

    def _calcola_hash(self, data_dict):
        chiavi = ["id", "pulsante_proposto", "pulsante_premuto", "tempo_risposta_ms"]
        dati_rilevanti = {k: data_dict[k] for k in chiavi if k in data_dict}
        json_ordinato = json.dumps(dati_rilevanti, sort_keys=True)
        return hashlib.sha256(json_ordinato.encode("utf-8")).hexdigest()
