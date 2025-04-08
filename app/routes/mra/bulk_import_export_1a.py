from flask import Flask, request, jsonify, current_app
from flask_restful import Api, Resource

import inspect

from utils.config import config, env
from utils.tracing.restful_logger_decorator import log_restful_class_on_any_method_call, log_restful_method_call

# -----------------------------------------------------------------------------

@log_restful_class_on_any_method_call(log_restful_method_call)
class BulkImportExport1A(Resource):
    """
    Gestisce le operazioni di IMPORT/EXPORT CRUD sull'intero database:
    """

    def get(self):
        """
        Ritorna (esporta) tutto l'intero database in bulk-downloading da root '/'
        ---
        tags:
          - MRA - Bulk Database IMPORT / EXPORT
        summary: Ottiene (esporta) in bulk-downloading il documento JSON per tutto l'intero database, rilevando tutti i livelli di profondità presenti.
        description: >
          Ritorna (esporta) in bulk-downloading il documento JSON per tutto l'intero database, rilevandone tutti i livelli di profondità presenti.
        responses:
          200:
            description: Root node del database esportato con successo in modalità bulk-downloading
          404:
            description: Nessun dato disponibile nel database da esportare in bulk-downloading
            examples:
              application/json:
                {
                  "error": "Nessun dato disponibile nel database da esportare"
                }
          500:
            description: Errore interno del server
            examples:
              application/json:
                {
                  "error": "<INTERNAL-EXCEPTION>",
                  "comment": "Errore interno del server in <ERROR-LOCATON>"
                }
        """
        try:
            # Generazione forzata di test per HTTP resp-code 500 (INTERNAL-SERVER-ERROR):
            # raise ValueError("Test per 500-INTERNAL-SERVER-ERROR")

            db = current_app.config['firebase'].get('db_app_1a')
            ref = db.get_reference("/") # <- export completo da root '/' (database bulk downloading)
            get_reply = ref.get()

            if not get_reply:
                return {"error": "Nessun dato disponibile nel database da esportare"}, 404

            # # Esempio: Aggiunta manuale dei link HATEOAS per ciascun atleta
            # response = []

            # for id_entity, entity_original_format in get_reply.items():
            #     entity_view_model = BulkImportExportViewModel(id_entity, entity_original_format)

            #     entity_view_model_dictionary = entity_view_model.to_dict()
            #     # etag = entity_view_model_dictionary["_hash"]

            #     response.append(entity_view_model_dictionary)

            # return response, 200

            return get_reply, 200

        except Exception as e:
            error_location = "BulkImportExport1A.get"
            print(f"❌ Errore in class {error_location} per GET / in database exporting via bulk-downloading: {e}")
            return {
                "error": str(e),
                "comment": f"Errore interno del server in {error_location}"
            }, 500

    #--------------------------------------------------------------------------
    def post(self):
        """
        Inserisce (importa) un intero database in bulk-loading, conservando invariato il formato dei dati in ingresso
        ---
        tags:
          - MRA - Bulk Database IMPORT / EXPORT
        summary: >
          Inserisce (importa) in bulk-downloading il documento JSON per un intero database, considerando tutti i >
          livelli di profondità presenti e conservando invariato il formato dei dati in ingresso.
        description: >
          Inserisce (importa) in bulk-loading il documento JSON per un database intero, considerandone tutti i livelli >
          di profondità presenti.
        responses:
          201:
            description: Database caricato (importato) con successo in bulk-loading
          400:
            description: Dati mancanti o malformati nel payload in ingresso
            examples:
              application/json:
                { "error": "Dati mancanti o malformati nel payload in ingresso" }
          409:
            description: Database non vuoto, quindi non posso procedere al bulk-loading!
            examples:
              application/json:
                { "error": "ID atleta già presente" }
          500:
            description: Errore interno del server
            examples:
              application/json:
                {
                  "error": "<INTERNAL-EXCEPTION>",
                  "comment": "Errore interno del server in <ERROR-LOCATON>"
                }
        """
        try:
            dati = request.get_json(force=True)

            # Validazione dati in ingresso (JSON Request Body):
            required_keys = ["tempiDiReazione"]
            if not all(k in dati for k in required_keys):
                return {"error": "Dati mancanti o malformati nel payload in ingresso"}, 400

            db = current_app.config['firebase'].get('db_app_1a')

            # Controlla se esiste già qualsiasi contenuto pre-esistente nel database
            ref = db.get_reference(f"/")
            if ref.get() is not None:
                return {"error": "Database non vuoto, quindi non posso procedere al bulk-loading!"}, 409

            # Prepara i dati da salvare (formato Firebase già presente per i dati in ingresso, trattandosi di bulk-loading)
            dati_firebase = dati
            # dati_firebase = {
            #     "nickname": dati["nickname"],
            #     "sesso": dati["genere"],
            #     "data": dati["data-inserimento"]
            # }

            # Scrivi su Firebase
            ref.set(dati_firebase)

            # Restituizione del il risultato senza riformattazione
            # (si conserva il formato originale Firebase dei dati in ingresso)
            return dati_firebase, 201

        except Exception as e:
            error_location = "BulkImportExport1A.post"
            print(f"❌ Errore in class {error_location} per POST / in database exporting via bulk-loading: {e}")
            return {
                "error": str(e),
                "comment": f"Errore interno del server in {error_location}."
            }, 500

    #--------------------------------------------------------------------------
    def delete(self):
        """
        WARNING: elimina (drop) un intero database in bulk-loading partendo da '/' root
        ---
        tags:
          - MRA - Bulk Database IMPORT / EXPORT
        summary: Elimina (drop) un intero database in bulk-loading partendo da '/' root
        responses:
          204:
            description: Intero database eliminato (dropped) con successo
          404:
            description: Nessun dato presente in database, database già vuoto
            examples:
              application/json:
                error: "Nessun dato presente in database, database già vuoto"
          500:
            description: Errore interno del server
            examples:
              application/json:
                error: "<EXCEPTION>"
                comment: "Errore interno del server in Atleta.delete"
        """
        try:

            db = current_app.config['firebase'].get('db_app_1a')
            ref = db.get_reference("/")
            if not ref.get():
                return {"error": "Nessun dato presente in database, database già vuoto"}, 404

            ref.delete()
            return '', 204

        except Exception as e:
            error_location = "BulkImportExport1A.delete"
            print(f"❌ Errore in {error_location}: {e}")
            return {"error": str(e), "comment": f"Errore interno del server in {error_location}"}, 500
