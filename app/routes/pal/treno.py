"""
Risorsa RESTful - Dettaglio di un treno transitato al passaggio a livello (PAL)

GET /api/pal/v1.0.0/storico-treni/<id_treno_encoded>

Restituisce i dettagli simulati di un treno, a partire da un timestamp registrato nel backup.
"""

from flask_restful import Resource
from flask import current_app
from urllib.parse import unquote
from app.routes.pal.view_models.treno_view_model import TrenoViewModel
from utils.tracing.restful_logger import log_restful_class_on_any_method_call, log_restful_method_call

# -----------------------------------------------------------------------------

@log_restful_class_on_any_method_call(log_restful_method_call)
class Treno(Resource):

    def __init__(self):
        self.firebase_db = current_app.config["FIREBASE"].get("db_app_1h")

    def get(self, id_treno_encoded):
        """
        Recupera i dettagli simulati di un treno a partire da un timestamp.
        """
        try:
            timestamp = unquote(id_treno_encoded)
            raw_data = self.firebase_db.get_reference("/pal/backup").get()

            if not raw_data or timestamp not in raw_data:
                return {"error": f"Nessun dato trovato per il treno {timestamp}"}, 404

            stato = int(raw_data[timestamp].replace("stato: ", "").strip())

            # Simulazione contenuti dettagliati: velocità, tratta, tipologia
            view_model = TrenoViewModel(
                id_treno=timestamp,
                stato=stato,
                velocita_kmh=round(60 + (stato * 40)),  # finta logica per demo
                tratta="Milano - Bologna" if stato % 2 == 0 else "Roma - Napoli",
                tipologia=["regionale", "intercity", "rapido", "altavelocita"][stato % 4]
            )

            return view_model.to_dict(), 200

        except Exception as e:
            return {"error": f"Errore durante il recupero treno: {str(e)}"}, 500
