"""
Risorsa RESTful - Stato Attuale del Passaggio a Livello (PAL)

GET /api/pal/v1.0.0/stato-attuale-passaggio

Restituisce lo stato attuale rilevato del passaggio a livello, con informazioni
sullo stato della sbarra, velocità del treno, e tempo di attesa accumulato.
"""

from flask_restful import Resource
from flask import current_app
from utils.firebase.firebase_initializer import FirebaseInitializer
from app.routes.pal.view_models.stato_attuale_passaggio_view_model import StatoAttualePassaggioViewModel
from utils.tracing.restful_logger_decorator import log_restful_class_on_any_method_call, log_restful_method_call

# -----------------------------------------------------------------------------

@log_restful_class_on_any_method_call(log_restful_method_call)
class StatoAttualePassaggio(Resource):
    """
    Rappresenta lo stato attuale del passaggio a livello, restituendo
    orario rilevazione, attesa accumulata e stato corrente della sbarra.
    """

    def __init__(self):
        self.firebase_db = current_app.config["firebase"].get("db_app_1h")

    def get(self):
        """
        Restituisce lo stato attuale del passaggio a livello
        ---
        tags:
          - PAL - Stato Attuale Passaggio
        summary: Ottiene lo stato attuale del passaggio a livello
        description: >
          Recupera lo stato corrente del passaggio a livello da Firebase,
          inclusi lo stato delle sbarre, la stima dell'attesa e il timestamp attuale.
        responses:
          200:
            description: Stato attuale recuperato con successo
            schema:
              type: object
              properties:
                orario-rilevazione:
                  type: string
                  example: "2025-04-06 10:30:00"
                stima-attesa-residua-min:
                  type: integer
                  example: 12
                transitabilita:
                  type: integer
                  description: |
                    0 = passaggio-agibile-aperto
                    1 = passaggio-interrotto-chiuso
                    2 = passaggio-in-riapertura
                    3 = passaggio-in-chiusura
                  example: 3
                transitabilita-descrizione:
                  type: string
                  example: "passaggio-interrotto-chiuso"
                velocita-rilevata-ultimo-treno-kmh:
                  type: integer
                  example: 120
                tratta-ultimo-treno:
                  type: string
                  example: "Meda - Milano Cadorna [S4]"
                tipologia-ultimo-treno:
                  type: string
                  enum: ["REG-Regionale", "IC-Intercity", "RPD-Rapido"]
                  example: "IC-Intercity"
          500:
            description: Errore interno del server
            examples:
              application/json:
                {
                  "error": "Errore nel recupero stato attuale: <dettaglio>"
                }
        """
        try:
            # Leggi lo stato corrente dal ramo 'statoCorrente' nel Firebase
            ref = self.firebase_db.get_reference("/passaggioLivello/statoCorrente")
            get_reply = ref.get()

            # Costruisci il ViewModel:
            view_model = StatoAttualePassaggioViewModel(dati_raw = get_reply)
            #DEBUG: print(f"view_model:\n{view_model}")

            return view_model.to_dict(), 200

        except Exception as e:
            return {
                "error": f"Errore nel recupero stato attuale: {str(e)}"
            }, 500
