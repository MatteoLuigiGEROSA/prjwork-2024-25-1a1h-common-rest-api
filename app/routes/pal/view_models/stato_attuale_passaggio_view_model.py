"""
ViewModel per lo stato attuale del passaggio a livello (PAL).

Espone:
- orario-rilevazione: timestamp corrente (epoch o formato leggibile)
- attesa-accumulata-sec: simulazione di tempo in secondi di sbarra chiusa
- transito: stato del passaggio (0=aperto, 1=chiuso, 2=in apertura, 3=in chiusura)

Include:
- _links per HATEOAS
- _hash per integrità contenuto
"""

import hashlib
import time

class StatoAttualePassaggioViewModel:

    def __init__(self, firebase_data: dict):
        stato_corrente = firebase_data.get("statoCorrente", {})
        codifica = firebase_data.get("codifica", {})

        self.orario_rilevazione = int(time.time())
        self.attesa_accumulata_sec = self._simula_attesa(stato_corrente)
        self.transito = stato_corrente.get("statoPassaggioLivello", 0)

        self._links = {
            "self": "/api/pal/v1.0.0/stato-attuale-passaggio"
        }

        self._hash = self._calcola_hash()

    def to_dict(self):
        return {
            "orario-rilevazione": self.orario_rilevazione,
            "attesa-accumulata-sec": self.attesa_accumulata_sec,
            "transito": self.transito,
            "_links": self._links,
            "_hash": self._hash
        }

    def _simula_attesa(self, stato_corrente: dict) -> int:
        stato = stato_corrente.get("statoPassaggioLivello", 0)
        velocita = stato_corrente.get("velocita", 0)
        if stato == 1:  # chiuso
            return min(120, max(velocita // 100, 10))  # simulazione arbitraria
        elif stato in [2, 3]:  # in transizione
            return 5
        return 0  # aperto

    def _calcola_hash(self) -> str:
        raw = f"{self.orario_rilevazione}{self.attesa_accumulata_sec}{self.transito}"
        return hashlib.sha256(raw.encode("utf-8")).hexdigest()
