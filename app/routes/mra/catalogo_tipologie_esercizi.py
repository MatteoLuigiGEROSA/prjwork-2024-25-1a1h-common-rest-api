from flask import request, make_response, current_app
from flask_restful import Resource

from app.routes.mra.view_models.tipologia_esercizio_view_model import TipologiaEsercizioViewModel

class CatalogoTipologieEsercizi(Resource):
    """
    Gestisce l'accesso al catalogo delle tipologie di esercizi (lista completa)
    """

    #--------------------------------------------------------------------------
    def get(self):
        """
        Restituisce la lista completa delle tipologie esercizi a catalogo
        ---
        tags:
          - Catalogo Tipologie Esercizi
        summary: Ottiene la lista di tutte le tipologie di esercizi a catalogo
        responses:
          200:
            description: Lista delle tipologie trovata con successo
            schema:
              type: array
              items:
                type: object
                properties:
                  id:
                    type: string
                    example: "111"
                  nome:
                    type: string
                    example: "test base"
                  numero_tentativi:
                    type: integer
                    example: 9
                  _hash:
                    type: string
                    example: "abc123hash"
                  _links:
                    type: object
                    properties:
                      self:
                        type: string
                        example: "/api/mra/v1.0.0/catalogo-tipologie-esercizi/111"
                      tentativi:
                        type: string
                        example: "/api/mra/v1.0.0/catalogo-tipologie-esercizi/111/tentativi"
          404:
            description: Nessuna tipologia esercizio trovata nel catalogo
            examples:
              application/json:
                error: "Nessuna tipologia trovata"
          500:
            description: Errore interno del server
            examples:
              application/json:
                error: "<EXCEPTION>"
                comment: "Errore interno del server in CatalogoTipologieEsercizi.get"
        """
        try:
            db = current_app.config['firebase'].get('db_app_1a')
            ref = db.get_reference("/tempiDiReazione/tipoEsercizio")
            dati_tipologie = ref.get()

            if not dati_tipologie:
                return {"error": "Nessuna tipologia trovata"}, 404

            response = []
            for id_tipologia, raw_data in dati_tipologie.items():
                vm = TipologiaEsercizioViewModel(id_tipologia, raw_data)
                response.append(vm.to_dict())

            return response, 200

        except Exception as e:
            print(f"\u274c Errore in CatalogoTipologieEsercizi.get: {e}")
            return {
                "error": str(e),
                "comment": "Errore interno del server in CatalogoTipologieEsercizi.get"
            }, 500
