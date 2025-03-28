from flask import current_app
from flask_restful import Resource
import inspect

from app.routes.mra.view_models.tipologia_esercizi_svolti_view_model import TipologiaEserciziSvoltiViewModel

class TipologieEserciziSvolti(Resource):
    """
    Restituisce l'elenco delle tipologie di esercizi svolti da un atleta
    """

    #--------------------------------------------------------------------------
    def get(self, id_atleta):
        """
        Restituisce l'elenco delle tipologie di esercizi svolti da un atleta
        ---
        tags:
          - Tipologie Esercizi Svolti
        summary: Ottiene tutte le tipologie di esercizi svolti da un atleta
        parameters:
          - name: id_atleta
            in: path
            required: true
            type: string
            description: L'ID univoco dell'atleta
            example: "123"
        responses:
          200:
            description: Elenco delle tipologie recuperato con successo
            schema:
              type: array
              items:
                type: object
                properties:
                  id:
                    type: string
                    example: "111"
                  _hash:
                    type: string
                    example: "abc123hash"
                  _links:
                    type: object
                    properties:
                      self:
                        type: string
                        example: "/api/mra/v1.0.0/atleti/123/tipologie-esercizi-svolti/111"
                      sessioni:
                        type: string
                        example: "/api/mra/v1.0.0/atleti/123/tipologie-esercizi-svolti/111/sessioni"
          404:
            description: Nessuna tipologia trovata per questo atleta
            examples:
              application/json:
                error: "Nessuna tipologia di esercizi trovata"
          500:
            description: Errore interno del server
            examples:
              application/json:
                error: "<EXCEPTION>"
                comment: "Errore interno del server in TipologieEserciziSvolti.get"
        """
        try:
            db = current_app.config['firebase'].get('db_app_1a')
            ref = db.get_reference(f"/tempiDiReazione/utenti/{id_atleta}/esercizi")
            esercizi_dict = ref.get()

            if not esercizi_dict:
                return {"error": "Nessuna tipologia di esercizi trovata"}, 404

            response = []
            for id_esercizio, sessioni in esercizi_dict.items():
                vm = TipologiaEserciziSvoltiViewModel(id_atleta, id_esercizio, sessioni)
                response.append(vm.to_dict())

            return response, 200

        except Exception as e:
            error_location = f"{self.__class__.__name__}.{inspect.currentframe().f_code.co_name}"
            print(f"❌ Errore in {error_location}: {e}")
            return {
                "error": str(e),
                "comment": f"Errore interno del server in {error_location}"
            }, 500
