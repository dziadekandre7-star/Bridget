import json 
import os 

PREFERENCES_FILE = "preferences.json"

def cargar_preferencias():
    if not os.path.exists(PREFERENCES_FILE):
        return {}
    
    try: 
        with open(PREFERENCES_FILE, "r", encoding="utf-8") as archivo: 
            return json.load(archivo)
    except (json.JSONDecodeError, FileNotFoundError):
        return {}
    
def guardar_preferencia(tipo, valor):
    preferencias = cargar_preferencias()

    preferencias[tipo] = valor

    with open(PREFERENCES_FILE, "w", encoding="utf-8") as archivo: json.dump(preferencias, archivo, ensure_ascii=False, indent=4)
    return True

def obtener_preferencia(tipo):
    preferencias = cargar_preferencias()
    return preferencias.get(tipo, None)