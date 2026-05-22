import os 
import webbrowser
import subprocess

EJECUTABLES = {
    "vscode": "code",
    "notepad": "notepad",
    "calc": "calc",
    "chrome": "chrome",
    "opera": "opera",
    "spotify": "spotify"
}

PROGRAMAS = {
    "opera": [
        r"C:\Users\lukad\AppData\Local\Programs\Opera\opera.exe",
        r"C:\Program Files\Opera\opera.exe",
        r"C:\Program Files (x86)\Opera\opera.exe"       
    ], 
    "chrome":[
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
    ],
    "vscode":[
        r"C:\Users\lukad\AppData\Local\Programs\Microsoft VS Code\Code.exe",
        r"C:\Program Files\Microsoft VS Code\Code.exe"
    ],
    "spotify":[
        r"C:\Users\lukad\AppData\Roaming\Spotify\Spotify.exe"
    ], 
    "discord":[
        r"C:\Users\lukad\AppData\Local\Discord\Update.exe"
    ],
    "notepad" : [],
    "calc": [],
    "pinterest": []
}

def abrir_programa(nombre_programa):
    nombre_programa = nombre_programa.lower().strip()
    if nombre_programa not in PROGRAMAS:
        return False
    
    rutas_posibles = PROGRAMAS[nombre_programa]

    for ruta in rutas_posibles:
        if os.path.exists(ruta):
            os.startfile(ruta)
            return True  

    try: 
        comando = EJECUTABLES.get(nombre_programa, nombre_programa)
        subprocess.Popen(comando, shell=True)

        return True
    except Exception:
       return False


def buscar_en_internet(consulta):
    if not consulta.strip():
        return False
    
    url = f"https://www.google.com/search?q={consulta.replace(' ', '+')}"
    webbrowser.open(url)
    return True
