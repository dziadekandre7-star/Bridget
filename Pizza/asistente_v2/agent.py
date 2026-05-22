import datetime
from core.brain import procesar_comando
from core.memory import obtener_nombre_preferido


class AssistantAgent:
    """Base agent wrapper for the assistant logic.

    This class provides a simple interface to process user input,
    keep the assistant name, and run a CLI loop similar to main.py.
    """

    def __init__(self, assistant_name="Rick"):
        self.assistant_name = assistant_name

    def get_greeting(self):
        hora = datetime.datetime.now().hour

        if 5 <= hora < 12:
            return "Buenos días, estoy listo para arrancar."
        elif 12 <= hora < 18:
            return "Buenas tardes, listo cuando vos quieras."
        return "Buenas noches, decime qué hacemos hoy."

    def handle_input(self, user_input):
        return procesar_comando(user_input, self.assistant_name)

    def run(self):
        print(f"{self.assistant_name}: {self.get_greeting()}")

        while True:
            nombre_usuario = obtener_nombre_preferido() or "André"
            user_input = input(f"{nombre_usuario}: ")

            if user_input.lower() in ["salir", "exit", "quit", "adiós", "adios"]:
                print(f"{self.assistant_name}: Nos vemos.")
                break

            respuesta = self.handle_input(user_input)
            print(f"{self.assistant_name}: {respuesta}")


def create_agent(name="Rick"):
    return AssistantAgent(name)


if __name__ == "__main__":
    agent = create_agent()
    agent.run()
