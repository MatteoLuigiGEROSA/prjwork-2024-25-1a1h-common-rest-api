from flask import request, make_response, current_app
from flask_restful import Resource

from firebase_admin import db
from app.routes.mra.view_models.atleta_view_model import AtletaViewModel
from utils.tracing.restful_logger_decorator import log_restful_class_on_any_method_call, log_restful_method_call

# -----------------------------------------------------------------------------

@log_restful_class_on_any_method_call(log_restful_method_call)
class Atleta(Resource):
    """
    Gestisce le operazioni CRUD su un singolo atleta
    """

    #--------------------------------------------------------------------------
    def get(self, id_atleta):
        """
        Ottiene i dettagli di un atleta specifico per ID
        ---
        tags:
          - MRA - Atleti
        summary: Ottiene i dettagli di un atleta
        parameters:
          - name: id_atleta
            in: path
            type: string
            required: true
            description: ID univoco dell'atleta
            example: "123"
        responses:
          200:
            description: Atleta trovato
            examples:
              application/json:
                id: "123"
                nickname: "speedy"
                genere: "M"
                data-inserimento: "3/2000"
                _hash: "abc123hash"
                _links:
                  self: "/api/mra/v1.0.0/atleti/123"
                  tipologie_esercizi_svolti: "/api/mra/v1.0.0/atleti/123/tipologie-esercizi-svolti"
          304:
            description: Contenuto non modificato (ETag match)
          404:
            description: Atleta non trovato
            examples:
              application/json:
                error: "Atleta non trovato"
          500:
            description: Errore interno del server
            examples:
              application/json:
                error: "<EXCEPTION>"
                comment: "Errore interno del server in Atleta.get"
        """
        try:
            db = current_app.config['firebase'].get('db_app_1a')
            ref = db.get_reference(f"/tempiDiReazione/utenti/{id_atleta}")
            get_reply = ref.get()

            if not get_reply:
                return {"error": "Atleta non trovato"}, 404

            atleta_vm = AtletaViewModel(id_atleta, get_reply)
            atleta_dict = atleta_vm.to_dict()
            etag = atleta_dict["_hash"]

            client_etag = request.headers.get("If-None-Match")
            if client_etag == etag:
                return make_response('', 304)

            response = make_response(atleta_dict, 200)
            response.headers["ETag"] = etag
            return response

        except Exception as e:
            error_location = "Atleta.get"
            print(f"\u274c Errore in {error_location}: {e}")
            return {
                "error": str(e),
                "comment": f"Errore interno del server in {error_location}"
            }, 500

    #--------------------------------------------------------------------------
    def put(self, id_atleta):
        """
        Sostituisce completamente i dati di un atleta esistente
        ---
        tags:
          - MRA - Atleti
        summary: Aggiorna completamente un atleta
        description: >
          Questo metodo implementa un "safe PUT":
          - Recupera il documento esistente da Firebase
          - Applica i nuovi dati forniti nel body (nickname, genere, data-inserimento)
          - Mantiene inalterati eventuali rami non forniti (es. "esercizi")
          - Sovrascrive il documento completo, assicurando l'integrità dei dati
        parameters:
          - name: id_atleta
            in: path
            required: true
            type: string
            example: "123"
          - name: body
            in: body
            required: true
            schema:
              required: [nickname, genere, data-inserimento]
              properties:
                nickname:
                  type: string
                genere:
                  type: string
                  enum: [M, F]
                data-inserimento:
                  type: string
        responses:
          200:
            description: Atleta aggiornato con successo
            examples:
              application/json:
                id: "123"
                nickname: "nuovo_nome"
                genere: "F"
                data-inserimento: "6/2001"
                _hash: "updatedhash"
                _links:
                  self: "/api/mra/v1.0.0/atleti/123"
                  tipologie_esercizi_svolti: "/api/mra/v1.0.0/atleti/123/tipologie-esercizi-svolti"
          400:
            description: Payload incompleto
            examples:
              application/json:
                error: "Dati mancanti nel payload"
          404:
            description: Atleta non trovato
            examples:
              application/json:
                error: "Atleta non trovato"
          500:
            description: Errore interno del server
            examples:
              application/json:
                error: "<EXCEPTION>"
                comment: "Errore interno del server in Atleta.put"
        """
        try:
            dati = request.get_json(force=True)
            required_keys = ["nickname", "genere", "data-inserimento"]
            if not all(k in dati for k in required_keys):
                return {"error": "Dati mancanti nel payload"}, 400

            db = current_app.config['firebase'].get('db_app_1a')
            ref = db.get_reference(f"/tempiDiReazione/utenti/{id_atleta}")

            get_reply = ref.get()
            if not get_reply:
                return {"error": "Atleta non trovato"}, 404

            # Recupero rami children da reimpostare as-is (es. "esercizi")
            esercizi_original = get_reply.get("esercizi", {})

            # Costruzione del nuovo stato da salvare (safe PUT)
            dati_firebase = {
                "nickname": dati["nickname"],
                "sesso": dati["genere"],
                "data": dati["data-inserimento"],
                "esercizi": esercizi_original
            }

            ref.set(dati_firebase)

            atleta_vm = AtletaViewModel(id_atleta, dati_firebase)
            return atleta_vm.to_dict(), 200

        except Exception as e:
            error_location = "Atleta.put"
            print(f"❌ Errore in {error_location}: {e}")
            return {"error": str(e), "comment": f"Errore interno del server in {error_location}"}, 500

    #--------------------------------------------------------------------------
    def patch(self, id_atleta):
        """
        Aggiorna parzialmente i dati di un atleta esistente
        ---
        tags:
          - MRA - Atleti
        summary: Aggiorna uno o più campi dell'atleta
        parameters:
          - name: id_atleta
            in: path
            required: true
            type: string
            example: "123"
          - name: body
            in: body
            required: true
            schema:
              properties:
                nickname:
                  type: string
                genere:
                  type: string
                  enum: [M, F]
                data-inserimento:
                  type: string
        responses:
          200:
            description: Atleta aggiornato
            examples:
              application/json:
                id: "123"
                nickname: "aggiornato"
                genere: "M"
                data-inserimento: "3/2000"
                _hash: "patchedhash"
                _links:
                  self: "/api/mra/v1.0.0/atleti/123"
                  tipologie_esercizi_svolti: "/api/mra/v1.0.0/atleti/123/tipologie-esercizi-svolti"
          400:
            description: Nessun campo valido fornito
            examples:
              application/json:
                error: "Nessun campo valido fornito"
          404:
            description: Atleta non trovato
            examples:
              application/json:
                error: "Atleta non trovato"
          500:
            description: Errore interno del server
            examples:
              application/json:
                error: "<EXCEPTION>"
                comment: "Errore interno del server in Atleta.patch"
        """
        try:
            dati = request.get_json(force=True)

            db_ref = current_app.config['firebase'].get('db_app_1a')
            ref = db_ref.get_reference(f"/tempiDiReazione/utenti/{id_atleta}")
            atleta_esistente = ref.get()
            if not atleta_esistente:
                return {"error": "Atleta non trovato"}, 404

            aggiornamenti = {}

            if "nickname" in dati:
                aggiornamenti["nickname"] = dati["nickname"]
            if "genere" in dati:
                aggiornamenti["sesso"] = dati["genere"]
            if "data-inserimento" in dati:
                aggiornamenti["data"] = dati["data-inserimento"]

            if not aggiornamenti:
                return {"error": "Nessun campo valido fornito"}, 400

            # ⚠️ PATCH: aggiorna solo i campi presenti nel payload.
            # Firebase manterrà automaticamente intatti tutti gli altri rami (es. "esercizi"):
            ref.update(aggiornamenti)

            atleta_aggiornato = ref.get()
            atleta_vm = AtletaViewModel(id_atleta, atleta_aggiornato)
            return atleta_vm.to_dict(), 200

        except Exception as e:
            error_location = "Atleta.patch"
            print(f"\u274c Errore in {error_location}: {e}")
            return {"error": str(e), "comment": f"Errore interno del server in {error_location}"}, 500

    #--------------------------------------------------------------------------
    def delete(self, id_atleta):
        """
        Elimina un atleta dal sistema
        ---
        tags:
          - MRA - Atleti
        summary: Elimina un atleta
        parameters:
          - name: id_atleta
            in: path
            required: true
            type: string
            example: "123"
        responses:
          204:
            description: Atleta eliminato con successo
          404:
            description: Atleta non trovato
            examples:
              application/json:
                error: "Atleta non trovato"
          500:
            description: Errore interno del server
            examples:
              application/json:
                error: "<EXCEPTION>"
                comment: "Errore interno del server in Atleta.delete"
        """
        try:
            db_ref = current_app.config['firebase'].get('db_app_1a')
            ref = db_ref.get_reference(f"/tempiDiReazione/utenti/{id_atleta}")
            if not ref.get():
                return {"error": "Atleta non trovato"}, 404

            ref.delete()
            return '', 204

        except Exception as e:
            error_location = "Atleta.delete"
            print(f"\u274c Errore in {error_location}: {e}")
            return {"error": str(e), "comment": f"Errore interno del server in {error_location}"}, 500

#==============================================================================
