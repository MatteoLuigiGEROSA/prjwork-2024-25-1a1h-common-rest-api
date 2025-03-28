from flask import current_app
from flask_restful import Resource
import inspect
import urllib.parse

from app.routes.mra.view_models.sessione_view_model import SessioneViewModel

class Sessione(Resource):
    """
    Restituisce i dettagli di una singola sessione di esercizio svolto da un atleta.
    """

    #--------------------------------------------------------------------------
    def get(self, id_atleta, id_esercizio, id_sessione_encoded):
        """
        Ottiene i dettagli di una singola sessione
        ---
        tags:
          - Sessioni
        summary: Dettagli di una sessione
        parameters:
          - name: id_atleta
            in: path
            required: true
            type: string
            example: "123"
          - name: id_esercizio
            in: path
            required: true
            type: string
            example: "111"
          - name: id_sessione_encoded
            in: path
            required: true
            type: string
            description: Timestamp codificato della sessione
            example: "12-3-2025_13%3A40%3A49"
        responses:
          200:
            description: Sessione trovata con successo
            examples:
              application/json:
                id: "12-3-2025_13:40:49"
                numero_rilevazioni: 9
                _hash: "abc123hash"
                _links:
                  self: "/api/mra/v1.0.0/atleti/123/tipologie-esercizi-svolti/111/sessioni/12-3-2025_13:40:49"
                  rilevazioni: "/api/mra/v1.0.0/atleti/123/tipologie-esercizi-svolti/111/sessioni/12-3-2025_13:40:49/rilevazioni"
          404:
            description: Sessione non trovata
            examples:
              application/json:
                error: "Sessione non trovata"
          500:
            description: Errore interno del server
            examples:
              application/json:
                error: "<EXCEPTION>"
                comment: "Errore interno del server in Sessione.get"
        """
        try:
            id_sessione = urllib.parse.unquote(id_sessione_encoded)

            db = current_app.config['firebase'].get('db_app_1a')
            ref = db.get_reference(f"/tempiDiReazione/utenti/{id_atleta}/esercizi/{id_esercizio}/{id_sessione}")
            rilevazioni = ref.get()

            if not rilevazioni:
                return {"error": "Sessione non trovata"}, 404

            vm = SessioneViewModel(id_atleta, id_esercizio, id_sessione, rilevazioni)
            return vm.to_dict(), 200

        except Exception as e:
            error_location = f"{self.__class__.__name__}.{inspect.currentframe().f_code.co_name}"
            print(f"❌ Errore in {error_location}: {e}")
            return {
                "error": str(e),
                "comment": f"Errore interno del server in {error_location}"
            }, 500
