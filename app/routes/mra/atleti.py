from flask import Flask, request, jsonify, current_app
from flask_restful import Api, Resource

import inspect

from utils.config import config, env
from utils.tracing.restful_logger_decorator import log_restful_class_on_any_method_call, log_restful_method_call

from app.routes.mra.view_models.atleta_view_model import AtletaViewModel

# -----------------------------------------------------------------------------

@log_restful_class_on_any_method_call(log_restful_method_call)
class Atleti(Resource):
    """
    Gestisce le operazioni CRUD sugli atleti
    """

    def get(self):
        """
        Ritorna la lista completa di tutti gli Atleti
        ---
        tags:
          - MRA - Atleti
        summary: Ottiene la lista di tutti gli atleti
        description: >
          Ritorna la lista di tutti gli atleti registrati nel sistema, con metadati principali e link HATEOAS per ogni atleta.
        responses:
          200:
            description: Lista di atleti trovata con successo
            schema:
              type: array
              items:
                type: object
                properties:
                  id:
                    type: string
                    example: "123"
                  nickname:
                    type: string
                    example: "speedy"
                  sesso:
                    type: string
                    enum: [M, F]
                    example: "M"
                  data:
                    type: string
                    example: "3/2000"
                  _hash:
                    type: string
                    example: "9de188d209b5c30b6d86e40d231ecddd53ab5584879b485b1d8edbd65b53b899"
                  _links:
                    type: object
                    properties:
                      self:
                        type: string
                        example: "/api/mra/v1.0.0/atleti/123"
                      tipologie_esercizi_svolti:
                        type: string
                        example: "/api/mra/v1.0.0/atleti/123/tipologie-esercizi-svolti"
          404:
            description: Nessun atleta trovato
            examples:
              application/json:
                {
                  "error": "Nessun atleta trovato"
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
            ref = db.get_reference("/tempiDiReazione/utenti")
            get_reply = ref.get()

            if not get_reply:
                return {"error": "Nessun atleta trovato"}, 404

            # Esempio: Aggiunta manuale dei link HATEOAS per ciascun atleta
            response = []

            for id_entity, entity_original_format in get_reply.items():
                entity_view_model = AtletaViewModel(id_entity, entity_original_format)

                entity_view_model_dictionary = entity_view_model.to_dict()
                # etag = entity_view_model_dictionary["_hash"]

                response.append(entity_view_model_dictionary)

            return response, 200

        except Exception as e:
            error_location = "Atleti.get"
            print(f"❌ Errore in class {error_location} per GET /atleti: {e}")
            return {
                "error": str(e),
                "comment": f"Errore interno del server in {error_location}"
            }, 500

    #--------------------------------------------------------------------------
    def post(self):
        """
        Crea un nuovo atleta
        ---
        tags:
          - MRA - Atleti
        summary: Crea un nuovo atleta
        description: >
          Inserisce un nuovo atleta nel sistema. L'ID deve essere fornito nel payload.
          Se l'ID esiste già, viene restituito un errore.
        parameters:
          - name: body
            in: body
            required: true
            schema:
              type: object
              required:
                - id
                - nickname
                - genere
                - data-inserimento
              properties:
                id:
                  type: string
                  example: "789"
                nickname:
                  type: string
                  example: "fulmine"
                genere:
                  type: string
                  enum: [M, F]
                  example: "M"
                data-inserimento:
                  type: string
                  example: "1/2002"
        responses:
          201:
            description: Atleta creato con successo
            schema:
              type: object
              properties:
                id:
                  type: string
                nickname:
                  type: string
                genere:
                  type: string
                data-inserimento:
                  type: string
                _hash:
                  type: string
                _links:
                  type: object
                  properties:
                    self:
                      type: string
                    tipologie_esercizi_svolti:
                      type: string
          400:
            description: Dati mancanti o malformati
            examples:
              application/json:
                { "error": "Dati mancanti nel payload" }
          409:
            description: L'atleta con lo stesso ID esiste già
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
            required_keys = ["id", "nickname", "genere", "data-inserimento"]
            if not all(k in dati for k in required_keys):
                return {"error": "Dati mancanti nel payload"}, 400

            id_atleta = str(dati["id"])

            # Controlla se esiste già l'atleta
            db = current_app.config['firebase'].get('db_app_1a')
            ref = db.get_reference(f"/tempiDiReazione/utenti/{id_atleta}")
            if ref.get() is not None:
                return {"error": "ID atleta già presente"}, 409

            # Prepara i dati da salvare (formato Firebase)
            dati_firebase = {
                "nickname": dati["nickname"],
                "sesso": dati["genere"],
                "data": dati["data-inserimento"]
            }

            # Scrivi su Firebase
            ref.set(dati_firebase)

            # Crea il ViewModel per restituire il risultato formattato
            atleta_vm = AtletaViewModel(id_atleta, dati_firebase)
            return atleta_vm.to_dict(), 201

        except Exception as e:
            error_location = "Atleti.post"
            print(f"❌ Errore in {error_location} per POST /atleti: {e}")
            return {
                "error": str(e),
                "comment": f"Errore interno del server in {error_location}."
            }, 500