"""
ViewModel per rappresentare i dettagli di un singolo treno transitato presso il passaggio a livello.

Contiene:
- id_treno
- velocita-rilevata_kmh
- tratta
- tipologia
- _links
- _hash
"""

import hashlib

class TrenoViewModel:

    def __init__(self, id_treno: str, stato: int, velocita_kmh: int, tratta: str, tipologia: str):
        self.id_treno = id_treno
        self.stato = stato
        self.velocita_kmh = velocita_kmh
        self.tratta = tratta
        self.tipologia = tipologia

    def to_dict(self):
        base_url = f"/api/pal/v1.0.0/storico-treni/{self.id_treno}"

        payload = {
            "id": self.id_treno,
            "velocita-rilevata_kmh": self.velocita_kmh,
            "tratta": self.tratta,
            "tipologia": self.tipologia,
            "_links": {
                "self": base_url,
                "storico_treni": "/api/pal/v1.0.0/storico-treni"
            }
        }

        hash_input = f"{self.id_treno}|{self.velocita_kmh}|{self.tratta}|{self.tipologia}"
        payload["_hash"] = hashlib.sha256(hash_input.encode()).hexdigest()

        return payload
