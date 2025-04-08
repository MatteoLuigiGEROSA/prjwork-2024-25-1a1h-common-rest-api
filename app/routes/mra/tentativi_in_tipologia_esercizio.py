from flask import request, current_app
from flask_restful import Resource

from app.routes.mra.view_models.tentativo_in_tipologia_esercizio_view_model import TentativoInTipologiaEsercizioViewModel
from utils.tracing.restful_logger_decorator import log_restful_class_on_any_method_call, log_restful_method_call

# -----------------------------------------------------------------------------

@log_restful_class_on_any_method_call(log_restful_method_call)
class TentativiInTipologiaEsercizio(Resource):
    """
    Restituisce la lista dei tentativi (sequenza) di una tipologia di esercizio specifica
    """

    #--------------------------------------------------------------------------
    def get(self, id_tipologia):
        """
        Ottiene la lista completa dei tentativi previsti per una tipologia esercizio
        ---
        tags:
          - MRA - Catalogo Tipologie Esercizi
        summary: Ottiene la sequenza completa dei tentativi per una specifica tipologia
        parameters:
          - name: id_tipologia
            in: path
            required: true
            type: string
            description: ID della tipologia di esercizio
            example: "111"
        responses:
          200:
            description: Lista dei tentativi restituita con successo
            schema:
              type: object
              properties:
                sequenza_tentativi:
                  type: array
                  items:
                    type: object
                    properties:
                      id:
                        type: integer
                        example: 0
                      pulsante_led:
                        type: integer
                        example: 5
                      tempo_max_disponibile_ms:
                        type: integer
                        example: 3000
                      intertempo_wait_ms:
                        type: integer
                        example: 2000
                count_totale_tentativi:
                  type: integer
                  example: 9
          404:
            description: Tipologia non trovata o senza sequenza
            examples:
              application/json:
                error: "Tipologia non trovata"
          500:
            description: Errore interno del server
            examples:
              application/json:
                error: "<EXCEPTION>"
                comment: "Errore interno del server in TentativiInTipologiaEsercizio.get"
        """
        try:
            db = current_app.config['firebase'].get('db_app_1a')
            ref = db.get_reference(f"/tempiDiReazione/tipoEsercizio/{id_tipologia}/sequenza")
            sequenza_data = ref.get()

            if not sequenza_data:
                return {"error": "Tipologia non trovata"}, 404

            sequenza_pulsanti = sequenza_data.get("sequenzaPulsanti", "")
            sequenza_tempo = sequenza_data.get("sequenzaTempo", "")
            sequenza_wait = sequenza_data.get("sequenzaWait", "")

            lista_pulsanti = [int(p) for p in sequenza_pulsanti.split(",") if p]
            lista_tempo = [int(t) for t in sequenza_tempo.split(",") if t]
            lista_wait = [int(w) for w in sequenza_wait.split(",") if w]

            sequenza_tentativi = []
            for i in range(len(lista_pulsanti)):
                vm = TentativoInTipologiaEsercizioViewModel(
                    id_tentativo=i,
                    pulsante_led=lista_pulsanti[i],
                    tempo_max=lista_tempo[i] if i < len(lista_tempo) else None,
                    intertempo_wait=lista_wait[i] if i < len(lista_wait) else None,
                    id_tipologia=id_tipologia
                )
                sequenza_tentativi.append(vm.to_dict())

            return {
                "sequenza_tentativi": sequenza_tentativi,
                "count_totale_tentativi": len(sequenza_tentativi)
            }, 200

        except Exception as e:
            print(f"\u274c Errore in TentativiInTipologiaEsercizio.get: {e}")
            return {
                "error": str(e),
                "comment": "Errore interno del server in TentativiInTipologiaEsercizio.get"
            }, 500
