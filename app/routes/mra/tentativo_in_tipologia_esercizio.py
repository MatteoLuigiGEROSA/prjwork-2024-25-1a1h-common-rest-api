from flask import request, make_response, current_app
from flask_restful import Resource
from urllib.parse import unquote

from app.routes.mra.view_models.singolo_tentativo_in_tipologia_esercizio_view_model import SingoloTentativoInTipologiaEsercizioViewModel

class TentativoInTipologiaEsercizio(Resource):
    """
    Gestisce l'accesso ai dettagli di un singolo tentativo all'interno di una tipologia di esercizio del catalogo
    """

    #--------------------------------------------------------------------------
    def get(self, id_tipologia, id_tentativo):
        """
        Ottiene i dettagli di un singolo tentativo (step) di una tipologia di esercizio
        ---
        tags:
          - Catalogo Tipologie Esercizi
        summary: Ottiene i dettagli di un tentativo specifico all'interno di una tipologia di esercizio
        parameters:
          - name: id_tipologia
            in: path
            required: true
            type: string
            description: ID della tipologia di esercizio
            example: "111"
          - name: id_tentativo
            in: path
            required: true
            type: integer
            description: Indice (0-based) del tentativo da recuperare
            example: 2
        responses:
          200:
            description: Dettaglio del tentativo trovato con successo
            schema:
              type: object
              properties:
                id:
                  type: integer
                  example: 2
                pulsante_led:
                  type: integer
                  example: 4
                tempo_max_disponibile_ms:
                  type: integer
                  example: 3000
                intertempo_wait_ms:
                  type: integer
                  example: 2000
                _hash:
                  type: string
                  example: "abc123hash"
                _links:
                  type: object
                  properties:
                    self:
                      type: string
                      example: "/api/mra/v1.0.0/catalogo-tipologie-esercizi/111/tentativi/2"
          404:
            description: Tentativo non trovato
            examples:
              application/json:
                error: "Tentativo non trovato"
          500:
            description: Errore interno del server
            examples:
              application/json:
                error: "<EXCEPTION>"
                comment: "Errore interno del server in TentativoInTipologiaEsercizio.get"
        """
        try:
            db = current_app.config['firebase'].get('db_app_1a')
            ref = db.get_reference(f"/tempiDiReazione/tipoEsercizio/{id_tipologia}/sequenza")
            sequenza_data = ref.get()

            if not sequenza_data:
                return {"error": "Tipologia o sequenza non trovata"}, 404

            vm = SingoloTentativoInTipologiaEsercizioViewModel(id_tipologia, id_tentativo, sequenza_data)
            return vm.to_dict(), 200

        except Exception as e:
            print(f"\u274c Errore in TentativoInTipologiaEsercizio.get: {e}")
            return {
                "error": str(e),
                "comment": "Errore interno del server in TentativoInTipologiaEsercizio.get"
            }, 500
