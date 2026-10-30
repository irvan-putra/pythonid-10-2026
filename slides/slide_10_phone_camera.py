import time, cv2, numpy as np, slide_2_yolo as yolo
from fastapi import WebSocket, WebSocketDisconnect
from slide_7_sensor import app

class PhoneCamera:  # YOLO only calls isOpened() and read(), so this can replace the webcam
    def __init__(self, webcam):
        self.webcam, self.frame, self.time = webcam, None, 0

    def isOpened(self):
        return True

    def read(self):
        while True:
            if self.frame is not None:
                frame, self.frame = self.frame, None
                return True, frame
            if time.time() - self.time > 1:  # the phone isn't streaming
                ok, frame = self.webcam.read()
                if ok:
                    return ok, frame
            time.sleep(0.01)

yolo.webcam = camera = PhoneCamera(yolo.webcam)

@app.websocket("/camera")
async def stream(ws: WebSocket):
    await ws.accept()
    try:
        while True:  # the phone sends a JPEG, waits for the reply, then sends the next one
            jpeg = np.frombuffer(await ws.receive_bytes(), np.uint8)
            camera.frame, camera.time = cv2.imdecode(jpeg, cv2.IMREAD_COLOR), time.time()
            await ws.send_text("📷 sent to YOLO")
    except WebSocketDisconnect:
        pass
