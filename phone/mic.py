import asyncio, pathlib, numpy as np
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse
from faster_whisper import WhisperModel

app, model = FastAPI(), WhisperModel("tiny.en", compute_type="int8")

def transcribe(audio):
    segments, _ = model.transcribe(audio, vad_filter=True)
    return " ".join(segment.text.strip() for segment in segments)

@app.get("/")
def page():
    return FileResponse(pathlib.Path(__file__).with_name("mic.html"))

@app.websocket("/audio")
async def audio(ws: WebSocket):
    await ws.accept()
    buffer = np.zeros(0, np.float32)
    try:
        while True:
            buffer = np.append(buffer, np.frombuffer(await ws.receive_bytes(), np.float32))
            if len(buffer) >= 32000:  # 2 seconds at 16 kHz
                text, buffer = await asyncio.to_thread(transcribe, buffer), np.zeros(0, np.float32)
                words = text.lower()
                command = "NEXT" if "next" in words else "BACK" if "back" in words else ""
                print(f"🎙 {text} {command}", flush=True)
                await ws.send_text(f"{text} {command}")
    except WebSocketDisconnect:
        print("phone disconnected", flush=True)
