#!/bin/bash
cd ~/proyectos/Pizza
source venv311/bin/activate
cd asistente_v2

uvicorn api:app --host 0.0.0.0 --port 8000 &
UVICORN_PID=$!

cleanup() {
    echo "Cerrando Rick web..."
    fuser -k 8000/tcp 2>/dev/null
    pkill $NGROK_PID 2>/dev/null
    exit 0
}

trap cleanup SIGINT SIGTERM

ngrok http 8000
NGROK_PID=$!

wait $NGROK_PID