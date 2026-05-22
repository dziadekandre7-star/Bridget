import pyautogui
import time
import ollama
from core.vision import capturar_pantalla, ver_pantalla

pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0.5

def clickear(x, y):
    pyautogui.click(x, y)

def escribir(texto):
    pyautogui.write(texto, interval=0.05)

def presionar(tecla):
    pyautogui.press(tecla)

def esperar(segundos):
    time.sleep(segundos)
def planificar_tarea(instruccion):
    prompt = f"""
Sos Rick, un agente que controla una PC con Arch Linux.
Tarea solicitada: {instruccion}

Describí en lenguaje natural y de forma concisa los pasos que vas a seguir para completar la tarea.
No ejecutes nada todavía, solo describí el plan.
"""
    respuesta = ollama.chat(
        model="llama3.2",
        messages=[{"role": "user", "content": prompt}]
    )
    return respuesta["message"]["content"]