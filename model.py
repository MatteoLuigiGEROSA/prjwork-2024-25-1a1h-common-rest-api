import json

# Load athletes table:
def carica_tabella_atleti():
    with open("table_atleti.json") as json_file:
        return json.load(json_file)

atleti = carica_tabella_atleti()
