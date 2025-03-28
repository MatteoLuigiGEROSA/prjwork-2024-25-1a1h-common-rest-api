import hashlib
import json

class AtletaViewModel:

    """
    Trasforma i dati grezzi di un atleta in un formato REST-API pronto (con HATEOAS e hash).
    """

    #--------------------------------------------------------------------------
    def __init__(self, id_entity, dati_raw):
        self.id = id_entity
        self.nickname = dati_raw.get("nickname")
        self.genere = dati_raw.get("sesso")
        self.data_inserimento = dati_raw.get("data")

    #--------------------------------------------------------------------------
    def to_dict(self):
        # Costruzione del dizionario base
        entity_dict = {
            "id": self.id,
            "nickname": self.nickname,
            "genere": self.genere,
            "data-inserimento": self.data_inserimento
        }

        # Aggiunta dell'hash calcolato
        entity_dict["_hash"] = self._calcola_hash(entity_dict)

        # Aggiunta dei link HATEOAS
        entity_dict["_links"] = {
            "self": f"/api/mra/v1.0.0/atleti/{self.id}",
            "tipologie_esercizi_svolti": f"/api/mra/v1.0.0/atleti/{self.id}/tipologie-esercizi-svolti"
        }

        return entity_dict

    #--------------------------------------------------------------------------
    def _calcola_hash(self, entity_dict):
        """
        Calcola un hash SHA256 del solo subset rilevante (esclusi _links HATEOAS ed _hash).
        """
        # Usa solo i campi "core" (non _hash, non _links HATEOAS)
        chiavi_rilevanti = ["id", "nickname", "genere", "data-inserimento"]
        dati = {k: entity_dict[k] for k in chiavi_rilevanti if k in entity_dict}
        json_ordinato = json.dumps(dati, sort_keys=True)
        return hashlib.sha256(json_ordinato.encode("utf-8")).hexdigest()

#==============================================================================
