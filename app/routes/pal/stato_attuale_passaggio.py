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
from utils.tracing.restful_logger import log_restful_class_on_any_method_call, log_restful_method_call
from datetime import datetime

# -----------------------------------------------------------------------------

@log_restful_class_on_any_method_call(log_restful_method_call)
class StatoAttualePassaggio(Resource):

    def __init__(self):
        self.firebase_db = current_app.config["FIREBASE"].get("db_app_1h")

    def get(self):
        """
        Recupera lo stato corrente dal database Firebase e lo trasforma in ViewModel.
        """
        # Leggi lo stato corrente dal ramo 'statoCorrente' nel Firebase
        ref = self.firebase_db.get_reference("statoCorrente")
        stato_corrente = ref.get()

        # Recupera campo 'statoPassaggioLivello'
        stato = stato_corrente.get("statoPassaggioLivello", 0)

        # Simulazione o calcolo tempo di attesa (accumulato) in secondi
        # Per ora fittizio, ma potrebbe essere misurato da timestamp storici
        attesa_accumulata_sec = 14 if stato in [1, 3] else 0

        # Timestamp corrente per orario rilevazione
        orario_rilevazione = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Costruisci il ViewModel e restituisci
        view_model = StatoAttualePassaggioViewModel(
            orario_rilevazione=orario_rilevazione,
            attesa_accumulata_sec=attesa_accumulata_sec,
            transito=stato
        )

        return view_model.to_dict(), 200
