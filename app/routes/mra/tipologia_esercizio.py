from flask import request, make_response, current_app
from flask_restful import Resource

from app.routes.mra.view_models.tipologia_esercizio_view_model import TipologiaEsercizioViewModel
from utils.tracing.restful_logger import log_restful_class_on_any_method_call, log_restful_method_call

@log_restful_class_on_any_method_call(log_restful_method_call)
class TipologiaEsercizio(Resource):
    """
    Gestisce l'accesso ai dettagli di una singola tipologia di esercizio
    """

    #--------------------------------------------------------------------------
    def get(self, id_tipologia):
        """
        Ritorna i dettagli di una singola tipologia esercizio
        ---
        tags:
          - Catalogo Tipologie Esercizi
        summary: Ottiene i dettagli di una tipologia di esercizio specifica
        parameters:
          - name: id_tipologia
            in: path
            required: true
            type: string
            description: ID della tipologia di esercizio
            example: "111"
        responses:
          200:
            description: Tipologia trovata con successo
            schema:
              type: object
              properties:
                id:
                  type: string
                  example: "111"
                nome:
                  type: string
                  example: "test base"
                numero_tentativi:
                  type: integer
                  example: 9
                _hash:
                  type: string
                  example: "abc123hash"
                _links:
                  type: object
                  properties:
                    self:
                      type: string
                      example: "/api/mra/v1.0.0/catalogo-tipologie-esercizi/111"
                    tentativi:
                      type: string
                      example: "/api/mra/v1.0.0/catalogo-tipologie-esercizi/111/tentativi"
          404:
            description: Tipologia non trovata
            examples:
              application/json:
                error: "Tipologia non trovata"
          500:
            description: Errore interno del server
            examples:
              application/json:
                error: "<EXCEPTION>"
                comment: "Errore interno del server in TipologiaEsercizio.get"
        """
        try:
            db = current_app.config['firebase'].get('db_app_1a')
            ref = db.get_reference(f"/tempiDiReazione/tipoEsercizio/{id_tipologia}")
            tipologia_data = ref.get()

            if not tipologia_data:
                return {"error": "Tipologia non trovata"}, 404

            vm = TipologiaEsercizioViewModel(id_tipologia, tipologia_data)
            return vm.to_dict(), 200

        except Exception as e:
            print(f"❌ Errore in TipologiaEsercizio.get: {e}")
            return {"error": str(e), "comment": "Errore interno del server in TipologiaEsercizio.get"}, 500
