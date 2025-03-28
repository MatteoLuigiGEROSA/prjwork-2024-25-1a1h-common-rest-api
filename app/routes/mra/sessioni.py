from flask import current_app
from flask_restful import Resource
import inspect

from app.routes.mra.view_models.sessione_view_model import SessioneViewModel

class Sessioni(Resource):
    """
    Restituisce la lista delle sessioni per una tipologia di esercizio svolto da un atleta.
    """

    #--------------------------------------------------------------------------
    def get(self, id_atleta, id_esercizio):
        """
        Ottiene l'elenco delle sessioni di una tipologia di esercizio svolto
        ---
        tags:
          - Sessioni
        summary: Elenco sessioni svolte in una tipologia di esercizio
        parameters:
          - name: id_atleta
            in: path
            type: string
            required: true
            example: "123"
          - name: id_esercizio
            in: path
            type: string
            required: true
            example: "111"
        responses:
          200:
            description: Lista di sessioni trovata con successo
            examples:
              application/json:
                [
                  {
                    "id": "12-3-2025_13:40:49",
                    "numero_rilevazioni": 9,
                    "_hash": "abc123hash",
                    "_links": {
                      "self": "/api/mra/v1.0.0/atleti/123/tipologie-esercizi-svolti/111/sessioni/12-3-2025_13:40:49",
                      "rilevazioni": "/api/mra/v1.0.0/atleti/123/tipologie-esercizi-svolti/111/sessioni/12-3-2025_13:40:49/rilevazioni"
                    }
                  }
                ]
          404:
            description: Nessuna sessione trovata
            examples:
              application/json:
                error: "Nessuna sessione trovata"
          500:
            description: Errore interno del server
            examples:
              application/json:
                error: "<EXCEPTION>"
                comment: "Errore interno del server in Sessioni.get"
        """
        try:
            db = current_app.config['firebase'].get('db_app_1a')
            ref = db.get_reference(f"/tempiDiReazione/utenti/{id_atleta}/esercizi/{id_esercizio}")
            sessioni_dict = ref.get()

            if not sessioni_dict:
                return {"error": "Nessuna sessione trovata"}, 404

            response = []
            for id_sessione, rilevazioni in sessioni_dict.items():
                vm = SessioneViewModel(id_atleta, id_esercizio, id_sessione, rilevazioni)
                response.append(vm.to_dict())

            return response, 200

        except Exception as e:
            error_location = f"{self.__class__.__name__}.{inspect.currentframe().f_code.co_name}"
            print(f"❌ Errore in {error_location}: {e}")
            return {
                "error": str(e),
                "comment": f"Errore interno del server in {error_location}"
            }, 500
