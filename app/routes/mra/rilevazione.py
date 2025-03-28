from flask import request, make_response, current_app
from flask_restful import Resource
from urllib.parse import unquote

from app.routes.mra.view_models.rilevazione_view_model import RilevazioneViewModel

class Rilevazione(Resource):
    """
    Gestisce la lettura (GET) di una singola rilevazione specifica.
    """

    #--------------------------------------------------------------------------
    def get(self, id_atleta, id_esercizio, id_sessione_encoded, id_rilevazione_encoded):
        """
        Ottiene i dettagli di una singola rilevazione effettuata in una sessione
        ---
        tags:
          - Rilevazioni
        summary: Recupera i dettagli di una rilevazione specifica
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
          - name: id_rilevazione_encoded
            in: path
            type: string
            required: true
            example: "1"
        responses:
          200:
            description: Rilevazione trovata e restituita
          404:
            description: Rilevazione non trovata
            examples:
              application/json:
                error: "Rilevazione non trovata"
          500:
            description: Errore interno del server
            examples:
              application/json:
                error: "<EXCEPTION>"
                comment: "Errore interno del server in Rilevazione.get"
        """
        try:
            db = current_app.config['firebase'].get('db_app_1a')

            id_sessione = unquote(id_sessione_encoded)
            id_rilevazione = unquote(id_rilevazione_encoded)

            ref = db.get_reference(f"/tempiDiReazione/utenti/{id_atleta}/esercizi/{id_esercizio}/{id_sessione}/{id_rilevazione}")
            valore_rilevazione = ref.get()

            if valore_rilevazione is None:
                return {"error": "Rilevazione non trovata"}, 404

            rilevazione_vm = RilevazioneViewModel(
                id_atleta, id_esercizio, id_sessione, id_rilevazione, valore_rilevazione
            )
            return rilevazione_vm.to_dict(), 200

        except Exception as e:
            print(f"❌ Errore in Rilevazione.get: {e}")
            return {"error": str(e), "comment": "Errore interno del server in Rilevazione.get"}, 500
