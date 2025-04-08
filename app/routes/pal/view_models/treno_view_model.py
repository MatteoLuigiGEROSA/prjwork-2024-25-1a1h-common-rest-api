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
from datetime import datetime

from app.routes.pal.utils.orario_treni import OrarioTreni
from utils.tracing.view_model_logger_decorator import log_view_model

#------------------------------------------------------------------------------

@log_view_model
class TrenoViewModel:

    orario_treni = OrarioTreni()

    def __init__(self, id_entity: str, dati_raw: dict):

        stato = int(dati_raw.replace("stato: ", "").strip())
        velocita = round(60 + (stato * 40))  # finta logica per demo

        dt_from_id_treno = datetime.strptime(id_entity, "%d-%m-%Y_%H:%M:%S")
        dt_riformattata_str = dt_from_id_treno.strftime("%Y-%m-%d %H:%M:%S")
        tratta = self.get_tratta(dt_riformattata_str)
        tipologia = self.get_tipologia(dt_riformattata_str)

        self.id_treno = id_entity
        self.stato = stato # <- dato non utilizzato
        self.velocita_kmh = velocita
        self.tratta = tratta
        self.tipologia = tipologia


    def to_dict(self):
        base_url = f"/api/pal/v1.0.0/storico-treni/{self.id_treno}"

        payload = {
            "id": self.id_treno,
            "velocita-rilevata-kmh": self.velocita_kmh,
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

    def get_tratta(self, id_treno: str) -> str:
        return self.orario_treni.get_tratta_by_id_treno(id_treno)

    def get_tipologia(self, id_treno: str) -> str:
        return self.orario_treni.get_tipologia_by_id_treno(id_treno)

