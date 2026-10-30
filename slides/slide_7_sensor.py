import time, pathlib, threading, cv2, numpy as np, uvicorn
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse
import slide_1_whisper as whisper, slide_2_yolo as yolo

# The phone's camera and mic replace the laptop's, over WebSockets (page: slide_8_sensor.html)
app = FastAPI()

@app.get("/")
def page():
    return FileResponse(pathlib.Path(__file__).with_name("slide_8_sensor.html"))

@app.websocket("/camera")
async def camera(ws: WebSocket):
    await ws.accept()
    try:
        while True:  # the phone sends a JPEG, waits for the reply, then sends the next one
            jpeg = np.frombuffer(await ws.receive_bytes(), np.uint8)
            yolo.phone.update(frame=cv2.imdecode(jpeg, cv2.IMREAD_COLOR), time=time.time())
            await ws.send_text("📷 sent to YOLO")
    except WebSocketDisconnect:
        pass

@app.websocket("/audio")
async def audio(ws: WebSocket):
    await ws.accept()
    buffer = np.zeros(0, np.float32)
    try:
        while True:
            buffer = np.append(buffer, np.frombuffer(await ws.receive_bytes(), np.float32))
            if len(buffer) >= 32000:  # 2 seconds at 16 kHz, like the laptop mic
                whisper.phone.put(buffer)
                buffer = np.zeros(0, np.float32)
    except WebSocketDisconnect:
        pass

def start(root, go):  # the phone opens http://<laptop-ip>:8000
    server = {"app": app, "host": "0.0.0.0", "port": 8000, "log_level": "warning"}
    threading.Thread(target=uvicorn.run, kwargs=server, daemon=True).start()
