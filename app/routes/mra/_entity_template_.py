from flask import Flask, request, jsonify
from flask_restful import Api, Resource

import urllib.parse

import firebase_admin
from firebase_admin import credentials, db

from flask_swagger_ui import get_swaggerui_blueprint
from flasgger import Swagger

from utils.config import config, env

# -----------------------------------------------------------------------------

class _entity_template_(Resource):

    """
    Gestisce le operazioni CRUD sugli/sulle entity
    """

    #--------------------------------------------------------------------------
    def get(self):
        """
        Ottiene la lista di tutti gli atleti
        ---
        responses:
          200:
            description: "Lista atleti recuperata con successo"
          404:
            description: "Nessun atleta trovato"
          500:
            description: "Errore interno del server"
        """
        try:
            ref = db.reference("/tempiDiReazione/utenti")
            get_reply = ref.get()
            if not get_reply:
                return {"error": "Nessun atleta trovato"}, 404
            return get_reply, 200
        except Exception:
            return {"error": "Errore interno del server, riprovare più tardi"}, 500

    #--------------------------------------------------------------------------
    def post(self):
        """
        Aggiunge un nuovo atleta
        ---
        responses:
          201:
            description: "Atleta creato con successo"
          400:
            description: "Dati mancanti o non validi"
          500:
            description: "Errore interno del server"
        """
        try:
            data = request.get_json()
            if not data or "id" not in data:
                return {"error": "Dati mancanti o non validi"}, 400

            ref = db.reference(f"/tempiDiReazione/utenti/{data['id']}")
            ref.set(data)
            return {"message": "Atleta creato con successo"}, 201
        except Exception:
            return {"error": "Errore interno del server, riprovare più tardi"}, 500

    #--------------------------------------------------------------------------
    def put(self):
        """
        Aggiorna un atleta esistente
        ---
        responses:
          200:
            description: "Atleta aggiornato con successo"
          400:
            description: "Dati mancanti o non validi"
          500:
            description: "Errore interno del server"
        """
        try:
            data = request.get_json()
            if not data or "id" not in data:
                return {"error": "Dati mancanti o non validi"}, 400

            ref = db.reference(f"/tempiDiReazione/utenti/{data['id']}")
            ref.update(data)
            return {"message": "Atleta aggiornato con successo"}, 200
        except Exception:
            return {"error": "Errore interno del server, riprovare più tardi"}, 500

    #--------------------------------------------------------------------------
    def patch(self):
        """
        Modifica parzialmente un atleta esistente
        ---
        responses:
          200:
            description: "Atleta parzialmente aggiornato con successo"
          400:
            description: "Dati mancanti o non validi"
          500:
            description: "Errore interno del server"
        """
        try:
            data = request.get_json()
            if not data or "id" not in data:
                return {"error": "Dati mancanti o non validi"}, 400

            ref = db.reference(f"/tempiDiReazione/utenti/{data['id']}")
            ref.update(data)
            return {"message": "Atleta parzialmente aggiornato con successo"}, 200
        except Exception:
            return {"error": "Errore interno del server, riprovare più tardi"}, 500

    #--------------------------------------------------------------------------
    def delete(self):
        """
        Elimina un atleta esistente
        ---
        responses:
          200:
            description: "Atleta eliminato con successo"
          400:
            description: "Dati mancanti o non validi"
          500:
            description: "Errore interno del server"
        """
        try:
            data = request.get_json()
            if not data or "id" not in data:
                return {"error": "Dati mancanti o non validi"}, 400

            ref = db.reference(f"/tempiDiReazione/utenti/{data['id']}")
            ref.delete()
            return {"message": "Atleta eliminato con successo"}, 200
        except Exception:
            return {"error": "Errore interno del server, riprovare più tardi"}, 500

#==============================================================================
