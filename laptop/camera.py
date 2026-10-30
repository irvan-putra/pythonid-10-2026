import time, pathlib, threading, cv2, numpy as np
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse
from ultralytics import YOLO

app, latest = FastAPI(), {"frame": None, "people": 0}

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

@app.get("/")
def page():
    return FileResponse(pathlib.Path(__file__).with_name("camera.html"))

@app.websocket("/camera")
async def camera(ws: WebSocket):
    await ws.accept()
    try:
        while True:  # the phone sends a JPEG, waits for the reply, then sends the next one
            jpeg = np.frombuffer(await ws.receive_bytes(), np.uint8)
            latest["frame"] = cv2.imdecode(jpeg, cv2.IMREAD_COLOR)
            await ws.send_text(f"👥 {latest['people']} people")
    except WebSocketDisconnect:
        print("phone disconnected", flush=True)
