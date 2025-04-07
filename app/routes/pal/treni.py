"""
Risorsa RESTful - Elenco storico dei treni transitati al passaggio a livello (PAL)

GET /api/pal/v1.0.0/storico-treni

Restituisce la lista di timestamp corrispondenti ai transiti dei treni,
rappresentati in forma semplificata per uso storico/consultazione.
"""

from flask_restful import Resource
from flask import current_app
from urllib.parse import quote

from utils.tracing.restful_logger import log_restful_class_on_any_method_call, log_restful_method_call

# -----------------------------------------------------------------------------

@log_restful_class_on_any_method_call(log_restful_method_call)
class Treni(Resource):

    def __init__(self):
        self.firebase_db = current_app.config["FIREBASE"].get("db_app_1h")

    def get(self):
        """
        Recupera i treni storici dal backup in Firebase.
        """
        try:
            raw_data = self.firebase_db.get_reference("/pal/backup").get()

            if not raw_data:
                return {"treni": [], "_comment": "Nessun treno registrato"}, 200

            treni = []
            for timestamp_str, stato in sorted(raw_data.items(), reverse=True):
                stato_num = stato.replace("stato: ", "").strip()
                treni.append({
                    "timestamp": timestamp_str,
                    "stato": int(stato_num),
                    "_links": {
                        "self": f"/api/pal/v1.0.0/storico-treni/{quote(timestamp_str)}"
                    }
                })

            return {"treni": treni}, 200

        except Exception as e:
            return {"error": f"Errore durante la lettura dello storico treni: {str(e)}"}, 500
