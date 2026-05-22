import json 
import os 

MEMORY_FILE = "memory.json"

def cargar_recuerdos():
    if not os.path.exists(MEMORY_FILE):
        return []
    
    try: 
        with open(MEMORY_FILE, "r", encoding="utf-8") as archivo:
            return json.load(archivo)
    except (json.JSONDecodeError, FileNotFoundError):
        return []
    
def guardar_recuerdo(recuerdo):
    recuerdos = cargar_recuerdos() 

    if recuerdo not in recuerdos: 
        recuerdos.append(recuerdo)

        with open(MEMORY_FILE, "w", encoding="utf-8") as archivo: json.dump(recuerdos, archivo, ensure_ascii=False, indent=4)

        return True
    return False

def leer_recuerdos():
    return cargar_recuerdos()

def olvidar_recuerdo(recuerdo):

    recuerdos = cargar_recuerdos()

    if recuerdo in recuerdos:
        recuerdos.remove(recuerdo)

        with open(MEMORY_FILE, "w", encoding="utf-8") as archivo: json.dump(recuerdos, archivo, ensure_ascii=False, indent=4)
        return True
    return False

def borrar_todos_los_recuerdos():
    with open(MEMORY_FILE, "w", encoding="utf-8") as archivo: json.dump([], archivo, ensure_ascii=False, indent=4)
    return True

def obtener_nombre_preferido():
    recuerdos = cargar_recuerdos() 

    disparadores = [
        "me puedes decir",
        "me podes decir",
        "puedes decirme",
        "podes decirme",
        "llamame ",
        "llámame ",
    ]

    for recuerdo in recuerdos: 
        recuerdo_normalizado = recuerdo.lower()

        for disparador in disparadores:
            if disparador in recuerdo_normalizado:
                inicio = recuerdo_normalizado.find(disparador) + len(disparador)
                nombre = recuerdo_normalizado[inicio:].strip(" ,¿?.,;:!")
                if nombre: 
                    return nombre.title()
    return None