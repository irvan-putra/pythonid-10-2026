import time, asyncio, pathlib, threading, cv2, numpy as np
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse
from faster_whisper import WhisperModel
from ultralytics import YOLO

# Serves phone.html: the phone's camera -> YOLO and its microphone -> Whisper, over WebSockets
app, latest = FastAPI(), {"frame": None, "people": 0}
speech = WhisperModel("tiny.en", compute_type="int8")

def detect():  # one thread runs YOLO and owns the laptop window
    model = YOLO("yolo11n-pose.pt")
    while True:
        frame, latest["frame"] = latest["frame"], None
        if frame is None:
            time.sleep(0.01)
            continue
        result = model(frame, verbose=False)[0]
        latest["people"] = len(result.boxes)
        cv2.imshow("Phone camera -> YOLO", result.plot())
        cv2.waitKey(1)

threading.Thread(target=detect, daemon=True).start()

def transcribe(audio):
    segments, _ = speech.transcribe(audio, vad_filter=True)
    return " ".join(segment.text.strip() for segment in segments)

@app.get("/")
def page():
    return FileResponse(pathlib.Path(__file__).with_name("phone.html"))

@app.websocket("/camera")
async def camera(ws: WebSocket):
    await ws.accept()
    try:
        while True:  # the phone sends a JPEG, waits for the reply, then sends the next one
            jpeg = np.frombuffer(await ws.receive_bytes(), np.uint8)
            latest["frame"] = cv2.imdecode(jpeg, cv2.IMREAD_COLOR)
            await ws.send_text(f"👥 {latest['people']} people")
    except WebSocketDisconnect:
        print("camera disconnected", flush=True)

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
        print("mic disconnected", flush=True)
