"""
Risorsa RESTful - Elenco storico dei treni transitati al passaggio a livello (PAL)

GET /api/pal/v1.0.0/storico-treni

Restituisce la lista di timestamp corrispondenti ai transiti dei treni,
rappresentati in forma semplificata per uso storico/consultazione.
"""

from flask_restful import Resource
from flask import current_app
from urllib.parse import quote

from app.routes.pal.view_models.treno_view_model import TrenoViewModel
from utils.tracing.restful_logger_decorator import log_restful_class_on_any_method_call, log_restful_method_call

# -----------------------------------------------------------------------------

@log_restful_class_on_any_method_call(log_restful_method_call)
class Treni(Resource):
    """
    Rappresenta la risorsa REST per la lista storica dei treni transitati
    al passaggio a livello (PAL).
    """

    def __init__(self):
        self.firebase_db = current_app.config["firebase"].get("db_app_1h")

    def get(self):
        """
        Restituisce l'elenco storico dei treni transitati
        ---
        tags:
          - PAL - Treni
        summary: Elenco storico dei treni transitati
        description: >
          Ritorna una lista di timestamp ordinati in ordine decrescente,
          relativi ai transiti dei treni rilevati al passaggio a livello.
          Ogni item contiene anche un link HATEOAS alla risorsa dettagliata del treno.
        responses:
          200:
            description: Elenco treni restituito correttamente
            schema:
              type: object
              properties:
                id:
                  type: string
                  example: "06-04-2025_10:30:25"
                velocita-rilevata-kmh:
                  type: integer
                  example: 120
                tratta:
                  type: string
                  example: "Meda - Milano Cadorna [S4]"
                tipologia:
                  type: string
                  enum: ["REG-Regionale", "IC-Intercity", "RPD-Rapido"]
                  example: "REG-Regionale"
                _hash:
                  type: string
                  example: "f23a67bce2aa4fe591a188f3c4c73fd..."
                _links:
                  type: object
                  properties:
                    self:
                      type: string
                      example: "/api/pal/v1.0.0/storico-treni/06-04-2025_10:30:25"
          500:
            description: Errore interno durante la lettura dei dati
            examples:
              application/json:
                {
                  "error": "Errore durante la lettura dello storico treni: <dettaglio>"
                }
        """
        try:
            get_reply = self.firebase_db.get_reference("/passaggioLivello/backup").get()

            if not get_reply:
                return {"error": "Nessun treno registrato nello storico-treni"}, 404

            response = []
            for id_entity, stato in sorted(get_reply.items(), reverse=True):
                entity_view_model = TrenoViewModel(id_entity = id_entity, dati_raw = stato)

                entity_view_model_dictionary = entity_view_model.to_dict()

                response.append(entity_view_model_dictionary)

            return response, 200

        except Exception as e:
            return {"error": f"Errore durante la lettura dello storico-treni: {str(e)}"}, 500
