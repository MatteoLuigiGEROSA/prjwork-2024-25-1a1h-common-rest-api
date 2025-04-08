"""
Risorsa RESTful - Dettaglio di un treno transitato al passaggio a livello (PAL)

GET /api/pal/v1.0.0/storico-treni/<id_treno_encoded>

Restituisce i dettagli di un treno, a partire da un timestamp registrato nel backup.
"""

from flask_restful import Resource
from flask import current_app
from urllib.parse import unquote
from app.routes.pal.view_models.treno_view_model import TrenoViewModel
from utils.tracing.restful_logger_decorator import log_restful_class_on_any_method_call, log_restful_method_call

# -----------------------------------------------------------------------------

@log_restful_class_on_any_method_call(log_restful_method_call)
class Treno(Resource):
    """
    Rappresenta una risorsa REST per il recupero dei dettagli di un singolo treno
    transitato al passaggio a livello (PAL).
    """

    def __init__(self):
        self.firebase_db = current_app.config["firebase"].get("db_app_1h")

    def get(self, id_treno_encoded):
        """
        Restituisce i dettagli del treno per il timestamp indicato.
        ---
        tags:
          - PAL - Treni
        summary: Ottiene i dettagli di un singolo treno transitato
        description: >
          Recupera i dettagli velocità, tratta, tipologia) di un treno passato al passaggio a livello,
          utilizzando un identificativo codificato (timestamp).
        parameters:
          - name: id_treno_encoded
            in: path
            required: true
            type: string
            description: Identificatore del treno codificato (timestamp del passaggio)
        responses:
          200:
            description: Dettagli del treno trovati correttamente
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
          404:
            description: Nessun dato trovato per l'identificativo specificato
            examples:
              application/json:
                {
                  "error": "Nessun dato trovato per il treno 06-04-2025_10:30:25"
                }
          500:
            description: Errore interno durante il recupero del treno
            examples:
              application/json:
                {
                  "error": "Errore durante il recupero treno: <dettaglio>"
                }
        """
        try:
            id_treno = unquote(id_treno_encoded)
            dati_raw = self.firebase_db.get_reference(f"/passaggioLivello/backup/{id_treno}").get()

            if not dati_raw:
                return {"error": f"Nessun dato trovato per il treno {id_treno}"}, 404

            # Presentazione contenuti dettagliati: velocità, tratta, tipologia
            view_model = TrenoViewModel(id_entity=id_treno, dati_raw = dati_raw)

            return view_model.to_dict(), 200

        except Exception as e:
            return {"error": f"Errore durante il recupero treno: {str(e)}"}, 500
