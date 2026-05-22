import base64
import ollama
from PIL import ImageGrab

def capturar_pantalla():
    captura = ImageGrab.grab()
    captura.save("/tmp/rick_pantalla.png")
    with open("/tmp/rick_pantalla.png", "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

def ver_pantalla(pregunta="¿Qué ves en esta pantalla?"):
    imagen_base64 = capturar_pantalla()
    respuesta = ollama.chat(
        model="llava",
        messages=[{
            "role": "user",
            "content": pregunta,
            "images": [imagen_base64]
        }]
    )
    return respuesta["message"]["content"]