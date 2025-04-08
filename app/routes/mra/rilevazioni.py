from flask import request, make_response, current_app
from flask_restful import Resource
from urllib.parse import unquote

from app.routes.mra.view_models.rilevazione_view_model import RilevazioneViewModel
from utils.tracing.restful_logger_decorator import log_restful_class_on_any_method_call, log_restful_method_call

# -----------------------------------------------------------------------------

@log_restful_class_on_any_method_call(log_restful_method_call)
class Rilevazioni(Resource):
    """
    Gestisce la lettura (GET) della lista di rilevazioni per una sessione specifica.
    """

    #--------------------------------------------------------------------------
    def get(self, id_atleta, id_esercizio, id_sessione_encoded):
        """
        Ottiene tutte le rilevazioni effettuate in una sessione
        ---
        tags:
          - MRA - Rilevazioni
        summary: Recupera la lista di tutte le rilevazioni per una sessione
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
          - name: id_sessione_encoded
            in: path
            type: string
            required: true
            example: "12-3-2025_13:40:49"
        responses:
          200:
            description: Lista di rilevazioni trovata e restituita
          404:
            description: Nessuna rilevazione trovata
            examples:
              application/json:
                error: "Nessuna rilevazione trovata"
          500:
            description: Errore interno del server
            examples:
              application/json:
                error: "<EXCEPTION>"
                comment: "Errore interno del server in Rilevazioni.get"
        """
        try:
            db = current_app.config['firebase'].get('db_app_1a')

            id_sessione = unquote(id_sessione_encoded)

            ref = db.get_reference(f"/tempiDiReazione/utenti/{id_atleta}/esercizi/{id_esercizio}/{id_sessione}")
            rilevazioni_lista = ref.get()

            if not rilevazioni_lista or not isinstance(rilevazioni_lista, list):
                return {"error": "Nessuna rilevazione trovata"}, 404

            response = []
            for idx, valore in enumerate(rilevazioni_lista):
                if valore is None:
                    continue  # ignora eventuali valori nulli
                vm = RilevazioneViewModel(
                    id_atleta, id_esercizio, id_sessione, str(idx), valore
                )
                response.append(vm.to_dict())

            return response, 200

        except Exception as e:
            print(f"❌ Errore in Rilevazioni.get: {e}")
            return {"error": str(e), "comment": "Errore interno del server in Rilevazioni.get"}, 500
