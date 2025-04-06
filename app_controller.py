from flask import Flask, request, jsonify
from flask_restful import Api, Resource

import traceback

import urllib.parse

from flask_swagger_ui import get_swaggerui_blueprint
from flasgger import Swagger

from utils.config import config, env
from utils.tracing.logger_utils import get_logger

from utils.firebase.firebase_initializer import FirebaseInitializer

# -----------------------------------------------------------------------------

from app.routes.mra.bulk_import_export_1a import BulkImportExport1A
from app.routes.mra.atleti import Atleti
from app.routes.mra.atleta import Atleta
from app.routes.mra.tipologie_esercizi_svolti import TipologieEserciziSvolti
from app.routes.mra.tipologia_esercizi_svolti import TipologiaEserciziSvolti
from app.routes.mra.sessioni import Sessioni
from app.routes.mra.sessione import Sessione
from app.routes.mra.rilevazioni import Rilevazioni
from app.routes.mra.rilevazione import Rilevazione

from app.routes.mra.catalogo_tipologie_esercizi import CatalogoTipologieEsercizi
from app.routes.mra.tipologia_esercizio import TipologiaEsercizio
from app.routes.mra.tentativi_in_tipologia_esercizio import TentativiInTipologiaEsercizio
from app.routes.mra.tentativo_in_tipologia_esercizio import TentativoInTipologiaEsercizio

# -----------------------------------------------------------------------------

from app.routes.pal.bulk_import_export_1h import BulkImportExport1H

# -----------------------------------------------------------------------------

# Inizializzazione logger flusso princilale Flask web-application (app_controller):
logger_name = "main_webapp_controller"
config_logger_level = config[env].APP_CONTROLLER_LOGGER_LOG_LEVEL
config_logger_mode = config[env].APP_CONTROLLER_LOGGER_LOG_CHANNELS

logger = get_logger(name=logger_name, level=config_logger_level, mode=config_logger_mode)

# -----------------------------------------------------------------------------

logger.info("$$$ START APPLICATION")

app = Flask(__name__)

swagger = Swagger(app)

# -----------------------------------------------------------------------------

# # Debug - stampa i parametri attuali della configurazione:
# print("-----  Configurazione attuale della web-application:  ----- -----")
# print(vars(config[env]))
# print("----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ")

# -----------------------------------------------------------------------------

# Recupero credenziali ed endpoint-url per i database principali Firebase:
firebase = FirebaseInitializer(config[env])
firebase.initialize_all()
app.config['firebase'] = firebase

# -----------------------------------------------------------------------------

# Configurazione Swagger-UI (generatore automatico documentaz. API):
SWAGGER_DOC_ENDPOINT = "/api/docs"         # URL accesso documentaz. in formato Swagger
SWAGGER_JSONFILE = "/static/swagger.json"  # Percorso al file Swagger JSON

# Inizializzazione Swagger-UI:
swagger_ui_blueprint = get_swaggerui_blueprint(SWAGGER_DOC_ENDPOINT, SWAGGER_JSONFILE)
app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_DOC_ENDPOINT)

# -----------------------------------------------------------------------------

# Creazione dell'API Flask-RESTful
api = Api(app)

mra_base_url = "/api/mra/v1.0.0"
pal_base_url = "/api/pal/v1.0.0"

# Aggiunta API di bulk IMPORT/EXPORT per l'intero database 1A:
api.add_resource(BulkImportExport1A, f"{mra_base_url}/")

# Aggiunta di tutte le API previste per questa REST-API web-application, verso il database 1A:

api.add_resource(Atleti,                  f"{mra_base_url}/atleti")
api.add_resource(Atleta,                  f"{mra_base_url}/atleti/<int:id_atleta>")
api.add_resource(TipologieEserciziSvolti, f"{mra_base_url}/atleti/<int:id_atleta>/tipologie-esercizi-svolti")
api.add_resource(TipologiaEserciziSvolti, f"{mra_base_url}/atleti/<int:id_atleta>/tipologie-esercizi-svolti/<int:id_esercizio>")
api.add_resource(Sessioni,                f"{mra_base_url}/atleti/<int:id_atleta>/tipologie-esercizi-svolti/<int:id_esercizio>/sessioni")
api.add_resource(Sessione,                f"{mra_base_url}/atleti/<int:id_atleta>/tipologie-esercizi-svolti/<int:id_esercizio>/sessioni/<path:id_sessione_encoded>")
api.add_resource(Rilevazioni,             f"{mra_base_url}/atleti/<int:id_atleta>/tipologie-esercizi-svolti/<int:id_esercizio>/sessioni/<path:id_sessione_encoded>/rilevazioni")
api.add_resource(Rilevazione,             f"{mra_base_url}/atleti/<int:id_atleta>/tipologie-esercizi-svolti/<int:id_esercizio>/sessioni/<path:id_sessione_encoded>/rilevazioni/<path:id_rilevazione_encoded>")

api.add_resource(CatalogoTipologieEsercizi,     f"{mra_base_url}/catalogo-tipologie-esercizi")
api.add_resource(TipologiaEsercizio,            f"{mra_base_url}/catalogo-tipologie-esercizi/<id_tipologia>")
api.add_resource(TentativiInTipologiaEsercizio, f"{mra_base_url}/catalogo-tipologie-esercizi/<id_tipologia>/tentativi")
api.add_resource(TentativoInTipologiaEsercizio, f"{mra_base_url}/catalogo-tipologie-esercizi/<id_tipologia>/tentativi/<int:id_tentativo>")

# Aggiunta API di bulk IMPORT/EXPORT per l'intero database 1H:
api.add_resource(BulkImportExport1H, f"{pal_base_url}/")

# CatalogoTipologieEsercizi
# GET     /catalogo-tipologie-esercizi
# POST    /catalogo-tipologie-esercizi

# TipologiaEsercizio
# GET     /catalogo-tipologie-esercizi/<id_tipologia>
# PUT     /catalogo-tipologie-esercizi/<id_tipologia>
# PATCH   /catalogo-tipologie-esercizi/<id_tipologia>
# DELETE  /catalogo-tipologie-esercizi/<id_tipologia>

# TentativiInTipologiaEsercizio
# GET     /catalogo-tipologie-esercizi/<id_tipologia>/tentativi
# POST    /catalogo-tipologie-esercizi/<id_tipologia>/tentativi

# TentativoInTipologiaEsercizio
# GET     /catalogo-tipologie-esercizi/<id_tipologia>/tentativi/<int:id_tentativo>
# PUT     /catalogo-tipologie-esercizi/<id_tipologia>/tentativi/<int:id_tentativo>
# PATCH   /catalogo-tipologie-esercizi/<id_tipologia>/tentativi/<int:id_tentativo>
# DELETE  /catalogo-tipologie-esercizi/<id_tipologia>/tentativi/<int:id_tentativo>

# TentativoInTipologiaEsercizioViewModel  tentativo_in_tipologia_esercizio_view_model.py
# TipologiaEsercizioViewModel             tipologia_esercizio_view_model.py

# -----------------------------------------------------------------------------
# --- Definizione Frontend web-site Endpoint(s)
# -----------------------------------------------------------------------------

@app.route('/')
def home():
    return "CFP Terragni di Meda, Project-work MRA (1A) e PAL (1H) A.S. 2024-25 - Flask web-server per le REST-API"

# -----------------------------------------------------------------------------

# Endpoint per esposizione standard dello schema Swagger JSON
@app.route('/swagger.json', methods=['GET'])
def swagger_json():
    """
    Restituisce la documentazione Swagger JSON dell'API
    ---
    responses:
      200:
        description: "Swagger JSON generato con successo"
      500:
        description: "Errore interno del server durante la generazione della documentazione"
        examples:
          application/json:
            { "error": "Errore interno del server, impossibile generare Swagger JSON" }
    """
    try:
        return jsonify(swagger.get_apispecs()), 200
    except Exception as e:
        return jsonify({
          "error": "Errore interno del server, impossibile generare Swagger JSON",
          "exception": str(e),                 # Converts the exception message to string
          "traceback": traceback.format_exc()  # Optional: Provides full stack trace
          }), 500
    #     return jsonify({"error": "Errore interno del server, impossibile generare Swagger JSON", "exception": " + Exception + "}), 500

# =============================================================================

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5010, debug=True)

# =============================================================================
