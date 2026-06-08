from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel
from core.brain import procesar_comando
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

ASSISTANT_NAME = "Rick"
API_KEY = "kyy007351andy's#key"  # cambiá esto por algo tuyo

class Mensaje(BaseModel):
    texto: str

@app.post("/chat")
async def chat(mensaje: Mensaje, x_api_key: str = Header(None)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="No autorizado")
    respuesta = procesar_comando(mensaje.texto, ASSISTANT_NAME)
    return {"respuesta": respuesta}

@app.get("/")
async def root():
    return FileResponse("static/index.html")