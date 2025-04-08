"""
ViewModel per lo stato attuale del passaggio a livello (PAL).

Espone:
- orario-rilevazione: timestamp corrente (epoch o formato leggibile)
- attesa-accumulata-sec: simulazione di tempo in secondi di sbarra chiusa
- transito: stato del passaggio (0=aperto, 1=chiuso, 2=in apertura, 3=in chiusura)

Include:
- _links per HATEOAS
- _hash per integrità contenuto
"""

import hashlib
from datetime import datetime
import random
from utils.config import config, env
from app.routes.pal.utils.orario_treni import OrarioTreni
from utils.tracing.view_model_logger_decorator import log_view_model

#------------------------------------------------------------------------------

@log_view_model
class StatoAttualePassaggioViewModel:

    orario_treni = OrarioTreni()

    INVALID_VELOCITA_TRENI_AT_PAL = 10000
    MIN_VELOCITA_TRENI_AT_PAL = config[env].MIN_VELOCITA_TRENI_AT_PAL
    MAX_VELOCITA_TRENI_AT_PAL = config[env].MAX_VELOCITA_TRENI_AT_PAL

    MIN_ATTESA_TRENI_AT_PAL_MIN     = config[env].MIN_ATTESA_TRENI_AT_PAL_MIN
    MAX_ATTESA_TRENI_AT_PAL_MIN     = config[env].MAX_ATTESA_TRENI_AT_PAL_MIN
    DEFAULT_ATTESA_TRENI_AT_PAL_MIN = config[env].DEFAULT_ATTESA_TRENI_AT_PAL_MIN

    PASSAGGIO_VOID_VALUE_LABEL  = config[env].PASSAGGIO_VOID_VALUE_LABEL
    PASSAGGIO_APERTO_TAG        = config[env].PASSAGGIO_APERTO_TAG
    PASSAGGIO_APERTO_LABEL      = config[env].PASSAGGIO_APERTO_LABEL
    PASSAGGIO_CHIUSO_TAG        = config[env].PASSAGGIO_CHIUSO_TAG
    PASSAGGIO_CHIUSO_LABEL      = config[env].PASSAGGIO_CHIUSO_LABEL
    PASSAGGIO_IN_APERTURA_TAG   = config[env].PASSAGGIO_IN_APERTURA_TAG
    PASSAGGIO_IN_APERTURA_LABEL = config[env].PASSAGGIO_IN_APERTURA_LABEL
    PASSAGGIO_IN_CHIUSURA_TAG   = config[env].PASSAGGIO_IN_CHIUSURA_TAG
    PASSAGGIO_IN_CHIUSURA_LABEL = config[env].PASSAGGIO_IN_CHIUSURA_LABEL


    def __init__(self, dati_raw: dict):
        PASSAGGIO_VOID_VALUE_TAG = -1
        stato_pal = dati_raw.get("statoPassaggioLivello", PASSAGGIO_VOID_VALUE_TAG)
        velocita_from_db = dati_raw.get("velocita", self.INVALID_VELOCITA_TRENI_AT_PAL)
        # codifica_dict = dati_raw.get("codifica", {})

        self.transitabilita = stato_pal
        self.transitabilita_descr = self._get_descr_transitabilita(stato_pal)
        self.orario_rilevazione = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.stima_attesa_residua_min = self._get_stima_attesa_residua(stato_pal)
        self.velocita_rilevata_ultimo_treno_kmh = self._get_velocita(velocita_from_db)
        self.tratta_ultimo_treno = self._get_tratta_treno(self.orario_rilevazione)
        self.tipologia_ultimo_treno = self._get_tipologia_treno(self.orario_rilevazione)

        self._links = {
            "self": "/api/pal/v1.0.0/stato-attuale-passaggio"
        }
        self._hash = self._calcola_hash()


    def to_dict(self):
        return {
            "orario-rilevazione": self.orario_rilevazione,
            "stima-attesa-residua-min": self.stima_attesa_residua_min,
            "transitabilita": self.transitabilita,
            "transitabilita-descrizione": self.transitabilita_descr,
            "velocita-rilevata-ultimo-treno-kmh": self.velocita_rilevata_ultimo_treno_kmh,
            "tratta-ultimo-treno": self.tratta_ultimo_treno,
            "tipologia-ultimo-treno": self.tipologia_ultimo_treno,
            "_links": self._links,
            "_hash": self._hash
        }


    def _get_velocita(self, velocita_from_db: int) -> int:
        velocita_from_db_valida = (velocita_from_db != self.INVALID_VELOCITA_TRENI_AT_PAL)
        velocita_from_db_valida = velocita_from_db_valida and (velocita_from_db >= int(self.MIN_VELOCITA_TRENI_AT_PAL))
        velocita_from_db_valida = velocita_from_db_valida and (velocita_from_db <= int(self.MAX_VELOCITA_TRENI_AT_PAL))

        if velocita_from_db_valida:
            return velocita_from_db
        else:
            return random.randint(int(self.MIN_VELOCITA_TRENI_AT_PAL), int(self.MAX_VELOCITA_TRENI_AT_PAL))


    def _get_stima_attesa_residua(self, stato_pal: int) -> int:
        if stato_pal == int(self.PASSAGGIO_CHIUSO_TAG) or stato_pal == int(self.PASSAGGIO_IN_CHIUSURA_TAG):
            return random.randint(int(self.MIN_ATTESA_TRENI_AT_PAL_MIN), int(self.MAX_ATTESA_TRENI_AT_PAL_MIN))
        elif stato_pal == int(self.PASSAGGIO_APERTO_TAG):
            return 0 # nessuna attesa: 0 minuti
        elif stato_pal == int(self.PASSAGGIO_IN_APERTURA_TAG):
            return 1 # attesa fittizia: 1 minuto
        return self.DEFAULT_ATTESA_TRENI_AT_PAL_MIN  # praticamente "chiuso per riparazioni"


    def _get_descr_transitabilita(self, transitabilita: int) -> str:
        if transitabilita == int(self.PASSAGGIO_APERTO_TAG):
            return self.PASSAGGIO_APERTO_LABEL
        elif transitabilita == int(self.PASSAGGIO_CHIUSO_TAG):
            return self.PASSAGGIO_CHIUSO_LABEL
        elif transitabilita == int(self.PASSAGGIO_IN_APERTURA_TAG):
            return self.PASSAGGIO_IN_APERTURA_LABEL
        elif transitabilita == int(self.PASSAGGIO_IN_CHIUSURA_TAG):
            return self.PASSAGGIO_IN_CHIUSURA_LABEL
        else:
            return self.PASSAGGIO_VOID_VALUE_LABEL


    def _get_tratta_treno(self, id_treno: str) -> str:
        return self.orario_treni.get_tratta_by_id_treno(id_treno)


    def _get_tipologia_treno(self, id_treno: str) -> str:
        return self.orario_treni.get_tipologia_by_id_treno(id_treno)


    def _calcola_hash(self) -> str:
        raw = f"{self.orario_rilevazione}{self.stima_attesa_residua_min}{self.transitabilita}"
        return hashlib.sha256(raw.encode("utf-8")).hexdigest()
