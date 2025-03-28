from flask import current_app
from flask_restful import Resource
import inspect

from app.routes.mra.view_models.tipologia_esercizi_svolti_view_model import TipologiaEserciziSvoltiViewModel

class TipologiaEserciziSvolti(Resource):
    """
    Restituisce i metadati di una singola tipologia di esercizio svolto
    """

    #--------------------------------------------------------------------------
    def get(self, id_atleta, id_esercizio):
        """
        Ottiene i dettagli di una tipologia di esercizio svolto da un atleta
        ---
        tags:
          - Tipologie Esercizi Svolti
        summary: Ottiene i metadati di una singola tipologia
        parameters:
          - name: id_atleta
            in: path
            type: string
            required: true
            description: ID univoco dell'atleta
            example: "123"
          - name: id_esercizio
            in: path
            type: string
            required: true
            description: ID della tipologia di esercizio svolto
            example: "111"
        responses:
          200:
            description: Tipologia trovata
            examples:
              application/json:
                id: "111"
                numero_sessioni: 5
                intervallo_date_sessioni:
                  prima_sessione: "10-3-2025_11:59:2"
                  ultima_sessione: "21-3-2025_8:51:11"
                _hash: "abc123hash"
                _links:
                  self: "/api/mra/v1.0.0/atleti/123/tipologie-esercizi-svolti/111"
                  sessioni: "/api/mra/v1.0.0/atleti/123/tipologie-esercizi-svolti/111/sessioni"
          404:
            description: Tipologia non trovata
            examples:
              application/json:
                error: "Tipologia di esercizio svolto non trovata"
          500:
            description: Errore interno del server
            examples:
              application/json:
                error: "<EXCEPTION>"
                comment: "Errore interno del server in TipologiaEserciziSvolti.get"
        """
        try:
            db = current_app.config['firebase'].get('db_app_1a')
            ref = db.get_reference(f"/tempiDiReazione/utenti/{id_atleta}/esercizi/{id_esercizio}")
            sessioni_dict = ref.get()

            if not sessioni_dict:
                return {"error": "Tipologia di esercizio svolto non trovata"}, 404

            vm = TipologiaEserciziSvoltiViewModel(id_atleta, id_esercizio, sessioni_dict)
            return vm.to_dict(), 200

        except Exception as e:
            error_location = f"{self.__class__.__name__}.{inspect.currentframe().f_code.co_name}"
            print(f"❌ Errore in {error_location}: {e}")
            return {
                "error": str(e),
                "comment": f"Errore interno del server in {error_location}"
            }, 500
