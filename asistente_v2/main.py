import datetime 
from core.brain import procesar_comando
from core.memory import obtener_nombre_preferido
from core.voice import hablar

ASSISTANT_NAME = "Rick"

def obtener_saludo(): 
    hora = datetime.datetime.now().hour 

    if 5 <= hora < 12:
        return "Buenos días, estoy listo para arrancar."

    elif 12 <= hora < 18:
        return "Buenas tardes, listo cuando vos quieras."

    else: 
        return "Buenas noches, decime qué hacemos hoy."

def main():
    saludo = obtener_saludo()
    print(f"{ASSISTANT_NAME}: {saludo}")   

    while True: 
        nombre_usuario = obtener_nombre_preferido() or "André"
        user_input = input(f"{nombre_usuario}: ")

        if user_input.lower() in ["salir", "exit", "quit", "adiós", "adios"]:
            print(f"{ASSISTANT_NAME}: Nos vemos.")
            break

        respuesta = procesar_comando(user_input, ASSISTANT_NAME)   
        print(f"{ASSISTANT_NAME}: {respuesta}") 
        hablar(respuesta)

if __name__ == "__main__":
    main()