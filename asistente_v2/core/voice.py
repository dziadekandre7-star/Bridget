import subprocess 
from TTS.api import TTS

MODELO = "tts_models/multilingual/multi-dataset/xtts_v2"
AUDIO_REFERENCIA = "assets/rick_voice.wav"
AUDIO_SALIDA = "/tmp/rick_respuesta.wav"

tts = TTS(model_name=MODELO, progress_bar=False).to("cuda")

def hablar(texto):
    tts.tts_to_file(
        text=texto,
        speaker_wav=AUDIO_REFERENCIA,
        language="es",
        file_path=AUDIO_SALIDA
    )
    subprocess.run(["paplay", AUDIO_SALIDA])
