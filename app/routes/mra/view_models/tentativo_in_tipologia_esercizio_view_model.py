class TentativoInTipologiaEsercizioViewModel:
    """
    ViewModel per rappresentare un singolo tentativo all'interno di una tipologia di esercizio.
    Utilizzato per la visualizzazione dettagliata della lista completa.
    """

    def __init__(self, id_tipologia, id_tentativo, pulsante_led, tempo_max, intertempo_wait):
        self.id = str(id_tentativo)
        self.pulsante_led = str(pulsante_led)
        self.tempo_max_disponibile_ms = str(tempo_max) if tempo_max is not None else None
        self.intertempo_wait_ms = str(intertempo_wait) if intertempo_wait is not None else None
        self.id_tipologia = id_tipologia

    def to_dict(self):
        output = {
            "id": self.id,
            "pulsante-led": self.pulsante_led,
            "tempo-max-disponibile-ms": self.tempo_max_disponibile_ms,
            "intertempo-wait-ms": self.intertempo_wait_ms,
            "_links": {
                "self": f"/api/mra/v1.0.0/catalogo-tipologie-esercizi/{self.id_tipologia}/tentativi/{self.id}",
                "catalogo_tipologia": f"/api/mra/v1.0.0/catalogo-tipologie-esercizi/{self.id_tipologia}"
            },
            "_hash": self._calcola_hash()
        }
        return output

    def _calcola_hash(self):
        import hashlib, json
        core = {
            "id": self.id,
            "pulsante-led": self.pulsante_led,
            "tempo-max-disponibile-ms": self.tempo_max_disponibile_ms,
            "intertempo-wait-ms": self.intertempo_wait_ms
        }
        json_ordinato = json.dumps(core, sort_keys=True)
        return hashlib.sha256(json_ordinato.encode("utf-8")).hexdigest()
