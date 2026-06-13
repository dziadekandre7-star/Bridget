import whisper
import sounddevice as sd
from scipy.io.wavfile import write

MODELO_WHISPER = whisper.load_model("base", device= "cpu")
ARCHIVO_TEMP = "/tmp/rick_escucha.wav"
DURACION = 5
FRECUENCIA = 16000

def escuchar():
    print("🎙️ Escuchando...")
    audio = sd.rec(int(DURACION * FRECUENCIA), samplerate=FRECUENCIA, channels=1, dtype='int16')
    sd.wait()
    write(ARCHIVO_TEMP, FRECUENCIA, audio)
    resultado = MODELO_WHISPER.transcribe(ARCHIVO_TEMP, language="es")
    return resultado["text"].strip()

def escuchar_audio(ruta_archivo):
    """Transcribe un archivo de audio WAV usando Whisper."""
    try:
        resultado = MODELO_WHISPER.transcribe(ruta_archivo, language="es")
        return resultado["text"].strip()
    except Exception as e:
        print(f"Error al transcribir: {e}")
        return None
