class OrarioTreni:
    """
    Classe per gestire un orario dei treni, considerandolo localizzato in una singola stazione
    (in prossimità di un prefissato Passaggio a Livello): passaggi ad orari programmati, considerando
    per semplicità un tipico ritardo per il treno come già inglobato nel risultato della scelta.
    """

    def __init__(self):
        self.cardinalita_tipologie = 3
        self.lista_tipologie_treni =  ["REG-Regionale", "IC-Intercity", "RPD-Rapido"]
        self.cardinalita_tratte = 58
        self.lista_tratte = [
            "Milano Rogoredo - Meda [S2]",
            "Milano Porta Vittoria - Meda [S2]",
            "Milano Dateo - Meda [S2]",
            "Milano Porta Venezia - Meda [S2]",
            "Milano Repubblica - Meda [S2]",
            "Milano Porta Garibaldi - Meda [S2]",
            "Milano Lancetti - Meda [S2]",
            "Milano Bovisa - Meda [S2]",
            "Milano Affori - Meda [S2]",
            "Milano Bruzzano Parco Nord - Meda [S2]",
            "Cormano-Cusano Milanino - Meda [S2]",
            "Paderno Dugnano - Meda [S2]",
            "Palazzolo Milanese - Meda [S2]",
            "Varedo - Meda [S2]",
            "Bovisio Masciago-Mombello - Meda [S2]",
            "Cesano Maderno - Meda [S2]",
            "Seveso - Meda [S2]",
            "Meda - Seveso [S2]",
            "Meda - Cesano Maderno [S2]",
            "Meda - Bovisio Masciago-Mombello [S2]",
            "Meda - Varedo [S2]",
            "Meda - Palazzolo Milanese [S2]",
            "Meda - Paderno Dugnano [S2]",
            "Meda - Cormano-Cusano Milanino [S2]",
            "Meda - Milano Bruzzano Parco Nord [S2]",
            "Meda - Milano Affori [S2]",
            "Meda - Milano Bovisa [S2]",
            "Meda - Milano Lancetti [S2]",
            "Meda - Milano Porta Garibaldi [S2]",
            "Meda - Milano Repubblica [S2]",
            "Meda - Milano Porta Venezia [S2]",
            "Meda - Milano Dateo [S2]",
            "Meda - Milano Porta Vittoria [S2]",
            "Meda - Milano Rogoredo [S2]",
            "Milano Cadorna - Meda [S4]",
            "Milano Domodossola - Meda [S4]",
            "Milano Bovisa - Meda [S4]",
            "Milano Affori - Meda [S4]",
            "Milano Bruzzano Parco Nord - Meda [S4]",
            "Cormano-Cusano Milanino - Meda [S4]",
            "Paderno Dugnano - Meda [S4]",
            "Palazzolo Milanese - Meda [S4]",
            "Varedo - Meda [S4]",
            "Bovisio Masciago-Mombello - Meda [S4]",
            "Cesano Maderno - Meda [S4]",
            "Seveso - Meda [S4]",
            "Meda - Seveso [S4]",
            "Meda - Cesano Maderno [S4]",
            "Meda - Bovisio Masciago-Mombello [S4]",
            "Meda - Varedo [S4]",
            "Meda - Palazzolo Milanese [S4]",
            "Meda - Paderno Dugnano [S4]",
            "Meda - Cormano-Cusano Milanino [S4]",
            "Meda - Milano Bruzzano Parco Nord [S4]",
            "Meda - Milano Affori [S4]",
            "Meda - Milano Bovisa [S4]",
            "Meda - Milano Domodossola [S4]",
            "Meda - Milano Cadorna [S4]"
        ]


    def hash_string_to_int(self, s: str) -> int:
        hash_value = 0
        for char in s:
            hash_value = (hash_value * 31 + ord(char)) % (10**9 + 7)
        return hash_value


    def get_tratta_by_id_treno(self, id_treno: str) -> str:
        indice_tratta = (self.hash_string_to_int(id_treno) % self.cardinalita_tratte)
        #DEBUG: print(f"indice_tratta: [{indice_tratta}]")
        return self.lista_tratte[indice_tratta]


    def get_tipologia_by_id_treno(self, id_treno: str) -> str:
        indice_tipologia = (self.hash_string_to_int(id_treno) % self.cardinalita_tipologie)
        #DEBUG: print(f"indice_tipologia: [{indice_tipologia}]")
        return self.lista_tipologie_treni[indice_tipologia]
