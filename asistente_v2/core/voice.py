import subprocess 
from TTS.api import TTS

MODELO = "tts_models/es/css10/vits"
AUDIO_SALIDA = "/tmp/rick_respuesta.wav"

tts = TTS(model_name=MODELO, progress_bar=False).to("cuda")

def hablar(texto):
    tts.tts_to_file(
        text=texto,
        file_path=AUDIO_SALIDA
    )
    subprocess.run(["paplay", AUDIO_SALIDA])
