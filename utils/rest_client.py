import requests

class RESTClient:

    def __init__(self, base_url):
        """
        Inizializza il client REST per comunicare con API esterne.
        :param base_url: URL base del server REST (es. http://127.0.0.1:5010)
        """
        self.base_url = base_url.rstrip("/")  # Rimuove eventuali slash finali
        self._initialize_client()


    def _initialize_client(self):
        """
        Crea una sessione HTTP persistente e imposta gli headers.
        """
        self.session = requests.Session()
        self.headers = {"User-Agent": "MyFlaskClient/1.0"}
        print(f"✅ REST Client inizializzato con base URL: {self.base_url}")


    def get_data(self, endpoint, timeout=5, verify_server_sslcert=True):
        """
        Recupera i dati dall'API REST esterna con gestione degli errori e auto-restart in caso di errore.
        :param endpoint: Endpoint specifico dell'API (es. /api/atleti)
        :param timeout: Tempo in secondi di attesa per la connessione (default: 5 sec)
        :param verify_server_sslcert: Richiesta di verifica di validità certificato SSL del server invocato (default: True)
        """
        api_url = f"{self.base_url}/{endpoint.lstrip('/')}"  # Costruisce l'URL finale
        print(f"Chiamata API esterna: {api_url}")

        try:
            response = self.session.get(api_url, headers=self.headers, timeout=timeout, verify=verify_server_sslcert)
            response.raise_for_status()
            return response.json(), response.status_code  # ✅ Restituisce sempre (data, status_code)

        except requests.exceptions.Timeout:
            print("⚠️ Timeout nell'accesso all'API")
            return {"error": "Timeout nella comunicazione con l'API"}, 504

        except requests.exceptions.ConnectionError:
            print("⚠️ Impossibile connettersi all'API")
            return {"error": "Server API non raggiungibile"}, 503

        except requests.exceptions.HTTPError as http_err:
            print(f"❌ Errore HTTP: {http_err}")
            return {"error": f"Errore HTTP: {http_err}"}, response.status_code

        except requests.exceptions.RequestException as req_err:
            print(f"❌ Errore generico nella richiesta: {req_err}")
            return {"error": "Errore imprevisto nella comunicazione con il server"}, 500

        except requests.exceptions.SSLError as ssl_err:
            print(f"❌ Errore SSL: {ssl_err}")
            return {"error": "Errore SSL durante la connessione al server"}, 495

        except Exception as e:
            print(f"❌ Errore critico non gestito: {e}")
            return {"error": "Errore interno del server"}, 500

